import argparse
import json
import logging
import os
import sys
from typing import Mapping

from aiohttp import web

from infrastructure.server.http.setup import setup_routes


def on_startup(conf: Mapping):
    """Return a startup handler with access to config"""

    async def startup_handler(app: web.Application):
        setup_routes(app)

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
