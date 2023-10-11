from fastapi import FastAPI

from app.rest.health_rest import router as health_router


def register_routers(app: FastAPI):
    app.include_router(health_router)
