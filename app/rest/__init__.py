from fastapi import FastAPI

from app.rest.card_rest import router as card_router
from app.rest.health_rest import router as health_router

routers = [
    card_router,
    health_router
]


def register_routers(app: FastAPI):
    for router in routers:
        app.include_router(router)
