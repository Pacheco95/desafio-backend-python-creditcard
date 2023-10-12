from fastapi import FastAPI

from app.rest.card_rest import router as card_router
from app.rest.health_rest import router as health_router
from app.rest.token_rest import router as token_router
from app.rest.user_rest import router as user_router

routers = [
    card_router,
    health_router,
    token_router,
    user_router,
]


def register_routers(app: FastAPI):
    for router in routers:
        app.include_router(router)
