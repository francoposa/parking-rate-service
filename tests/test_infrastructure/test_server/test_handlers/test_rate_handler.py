from typing import List

from app.infrastructure.server.handlers.rate import DATETIME_FMT
from app.infrastructure.server.setup import RATE_PATH
from app.usecases.resources.rate import Rate


async def test_get_success(web_client):
    response = await web_client.get(
        RATE_PATH,
        params={
            "start_timestamp": "2015-07-01T07:00:00-05:00",
            "end_timestamp": "2015-07-01T12:00:00-05:00",
        },
    )
    response_body = await response.json()
    assert response_body["price"] == 1750

    response = await web_client.get(
        RATE_PATH,
        params={
            "start_timestamp": "2015-07-04T15:00:00+00:00",
            "end_timestamp": "2015-07-04T20:00:00+00:00",
        },
    )
    response_body = await response.json()
    assert response_body["price"] == 2000

    response = await web_client.get(
        RATE_PATH,
        params={
            "start_timestamp": "2015-07-04T07:00:00+05:00",
            "end_timestamp": "2015-07-04T20:00:00+05:00",
        },
    )
    response_body = await response.json()
    assert response_body["price"] == "Unavailable"


async def test_get_error(web_client):
    # Test invalid date format
    response = await web_client.get(
        RATE_PATH,
        params={
            "start_timestamp": "2015-07-0113:00:00-05:00",
            "end_timestamp": "2015-07-0112:00:00-05:00",
        },
    )
    response_body = await response.json()
    assert (
        response_body["error"]
        == f"start and end timestamp must be in format {DATETIME_FMT}"
    )

    # Test start timestamp after end timestamp
    response = await web_client.get(
        RATE_PATH,
        params={
            "start_timestamp": "2015-07-01T13:00:00-05:00",
            "end_timestamp": "2015-07-01T12:00:00-05:00",
        },
    )
    response_body = await response.json()
    assert response_body["error"] == "start timestamp must be before end timestamp"

    # Test start and end timestamps with different dates
    response = await web_client.get(
        RATE_PATH,
        params={
            "start_timestamp": "2015-07-01T13:00:00-05:00",
            "end_timestamp": "2015-07-02T15:00:00-05:00",
        },
    )
    response_body = await response.json()
    assert (
        response_body["error"]
        == "start timestamp and end timestamp must be on the same date"
    )


async def test_post_success(web_client, rate_post):

    # POST
    resp = await web_client.post(RATE_PATH, json=rate_post)
    assert resp.status == 200

    # Prices have changed
    response = await web_client.get(
        RATE_PATH,
        params={
            "start_timestamp": "2015-07-01T07:00:00-05:00",
            "end_timestamp": "2015-07-01T12:00:00-05:00",
        },
    )
    response_body = await response.json()
    assert response_body["price"] == 1200

    response = await web_client.get(
        RATE_PATH,
        params={
            "start_timestamp": "2015-07-04T15:00:00+00:00",
            "end_timestamp": "2015-07-04T20:00:00+00:00",
        },
    )
    response_body = await response.json()
    assert response_body["price"] == 1000

    # Sundays no longer available
    response = await web_client.get(
        RATE_PATH,
        params={
            "start_timestamp": "2019-09-15T02:00:00+05:00",
            "end_timestamp": "2019-09-15T05:00:00+05:00",
        },
    )
    response_body = await response.json()
    assert response_body["price"] == "Unavailable"


async def test_post_error(web_client, rate_repo, rate_post):

    # Get rates before POST
    baseline_rates: List[Rate] = rate_repo._data

    # Make one of the new JSON rates invalid with an unsupported timezone
    rate_post["rates"][0]["tz"] = "Amrica/Chicago"

    # POST rates where one has invalid timezone
    response = await web_client.post(RATE_PATH, json=rate_post)

    # Assert expected failure
    assert response.status == 400
    response_body = await response.json()
    assert response_body["error"] == "supplied JSON contains invalid rate objects"

    # Assert no effect on rates in app
    assert baseline_rates == rate_repo._data
