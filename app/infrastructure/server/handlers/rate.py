import json
from datetime import datetime
from typing import Optional, List

from aiohttp import web
from multidict import MultiMapping

from app.infrastructure.server.adapters.rate import deserialize_rates
from app.infrastructure.server.app_constants import RATE_REPO
from app.usecases.interfaces import IRateRepo
from app.usecases.resources.rate import Rate

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
    except Exception:
        raise web.HTTPBadRequest(
            text=json.dumps(
                {"error": f"start and end timestamp must be in format {DATETIME_FMT}"}
            ),
            content_type="application/json",
        )

    # Attempt to get matching rate
    rate_repo: IRateRepo = request.app[RATE_REPO]
    try:
        rate: Optional[Rate] = await rate_repo.get_rate_for_time_range(
            start_timestamp, end_timestamp
        )
    except IRateRepo.TimeRangeError as e:
        raise web.HTTPBadRequest(
            text=json.dumps({"error": str(e)}), content_type="application/json"
        )

    if not rate:
        # Valid request, but no rates exist for this time period
        return web.json_response({"price": "Unavailable"})

    # Single matching rate found. Return its price.
    return web.json_response({"price": rate.price})


async def post_rates(request: web.Request) -> web.Response:
    rate_repo: IRateRepo = request.app[RATE_REPO]

    try:
        post_data = await request.json()
    except Exception:
        raise web.HTTPBadRequest(
            text=json.dumps(
                {"error": "supplied JSON is invalid."}, content_type="application/json"
            )
        )

    try:
        json_rates = post_data["rates"]
        rates: List[Rate] = deserialize_rates(json_rates)
        await rate_repo.set_rates(rates)
    except Exception:
        raise web.HTTPBadRequest(
            text=json.dumps({"error": "supplied JSON contains invalid rate objects"}),
            content_type="application/json",
        )
    return web.json_response({"message": "New rates posted"})
