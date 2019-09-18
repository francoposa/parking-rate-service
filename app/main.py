import argparse
import json
import logging
import os
import sys
from typing import Mapping, List

from aiohttp import web

from app.infrastructure.datatastore.in_memory.repos.rate import InMemoryRateRepo
from app.infrastructure.server.adapters.rate import deserialize_rates
from app.infrastructure.server.app_constants import RATE_REPO
from app.infrastructure.server.setup import setup_routes, register_dependency
from app.usecases.interfaces import IRateRepo
from app.usecases.resources.rate import Rate


def on_startup(conf: Mapping):
    """Return a startup handler with access to config"""

    async def startup_handler(app: web.Application):
        setup_routes(app)

        # Set up rate repo, load rates, and register the repo with the app
        rate_repo: IRateRepo = InMemoryRateRepo()
        rates_file = open(conf["rates"]["rates_filepath"])
        rates: List[Rate] = deserialize_rates(json.load(rates_file)["rates"])
        await rate_repo.set_rates(rates)
        register_dependency(app, RATE_REPO, rate_repo)

    return startup_handler


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--config", "-c", help="JSON config file")
    arg_parser.add_argument(
        "-l",
        "--level",
        default=os.environ.get("LOG_LEVEL", "INFO"),
        help="Logging level",
    )
    args = arg_parser.parse_args()

    conf: Mapping = json.load(open(args.config))
    logging.basicConfig(level=args.level)

    app = web.Application()
    app.on_startup.append(on_startup(conf))
    web.run_app(app, host=conf["http"]["host"], port=conf["http"]["port"])


if __name__ == "__main__":
    sys.exit(main())
