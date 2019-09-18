import json
from typing import List

import pytest
from aiohttp import web

from app.infrastructure.datatastore.in_memory.repos.rate import InMemoryRateRepo
from app.infrastructure.server.adapters.rate import deserialize_rates
from app.infrastructure.server.app_constants import RATE_REPO
from app.infrastructure.server.setup import setup_routes, register_dependency
from app.usecases.interfaces import IRateRepo
from app.usecases.resources.rate import Rate


@pytest.fixture
def rate_post():
    return json.load(open("./tests/stubs/rates/POST.json"))


@pytest.fixture
async def rate_repo():
    rate_repo: IRateRepo = InMemoryRateRepo()
    initial_rates_file = open("./tests/stubs/rates/initial_rates.json")
    rates: List[Rate] = deserialize_rates(json.load(initial_rates_file)["rates"])
    await rate_repo.set_rates(rates)
    return rate_repo


@pytest.fixture
def web_app(loop, rate_repo):
    async def startup_handler(app):
        # Register all routes
        setup_routes(app)
        register_dependency(app, RATE_REPO, rate_repo)

    app = web.Application()
    app.on_startup.append(startup_handler)
    return app


@pytest.fixture
async def web_client(aiohttp_client, web_app):
    client = await aiohttp_client(web_app)
    return client
