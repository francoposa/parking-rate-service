from typing import Any

from aiohttp import web

from infrastructure.server.handlers import health, rate

HEALTH_PATH = "/health"
RATE_PATH = "/api/v1/rates"


def setup_routes(app):
    app.router.add_get(HEALTH_PATH, health.health)

    app.router.add_get(RATE_PATH, rate.get_rates)
    app.router.add_post(RATE_PATH, rate.post_rates)


def register_dependency(app: web.Application, constant_key: str, dependency: Any):
    """Add dependencies used by the HTTP handlers."""
    app[constant_key] = dependency
