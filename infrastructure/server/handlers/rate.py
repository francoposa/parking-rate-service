import json
from datetime import datetime
from typing import Optional

from aiohttp import web
from multidict import MultiMapping

from infrastructure.server.app_constants import RATE_REPO
from usecases.interfaces import IRateRepo
from usecases.resources.rate import Rate

DATETIME_FMT = "%Y-%m-%dT%H:%M:%S%z"  # ISO-8601


async def get_rates(request: web.Request) -> web.Response:

    # Parse start & end time parameters from query string
    query_map: MultiMapping = request.query
    try:

        start_timestamp: datetime = datetime.strptime(
            query_map["start_timestamp"], DATETIME_FMT
        )
        end_timestamp: datetime = datetime.strptime(
            query_map["end_timestamp"], DATETIME_FMT
        )
    except Exception as e:
        raise web.HTTPUnprocessableEntity(
            text=json.dumps(
                {"error": f"start and end timestamp must be in format {DATETIME_FMT}"}
            )
        )

    # Attempt to get matching rate
    rate_repo: IRateRepo = request.app[RATE_REPO]
    try:
        rate: Optional[Rate] = await rate_repo.get_rate_for_time_range(
            start_timestamp, end_timestamp
        )
    except IRateRepo.TimeRangeError as e:
        raise web.HTTPUnprocessableEntity(text=json.dumps({"errors": [str(e)]}))

    if not rate:
        # Valid request, but no rates exist for this time period
        return web.json_response({"message": "No rate found for this time range"})

    # Single matching rate found. Return its price.
    return web.json_response({"price": rate.price})


async def post_rates(request: web.Request) -> web.Response:
    rate_repo: IRateRepo = request.app[RATE_REPO]

    try:
        post_data = await request.json()
    except Exception:
        raise web.HTTPBadRequest(
            text=json.dumps({"errors": ["The supplied JSON is invalid."]})
        )

    try:
        json_rates = post_data["rates"]
        await rate_repo.set_rates(json_rates)
    except Exception:
        raise web.HTTPUnprocessableEntity(
            text=json.dumps(
                {"errors": ["The supplied JSON does not contain valid rate objects"]}
            )
        )
    return web.json_response({"message": "New rates posted"})
