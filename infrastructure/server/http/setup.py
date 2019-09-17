from infrastructure.server.http.handlers import health

HEALTH_PATH = "/health"
HEALTH_NAME = "health"

def setup_routes(app):
    app.router.add_get(HEALTH_PATH, health.health, name=HEALTH_NAME)