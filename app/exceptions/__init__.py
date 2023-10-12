import pymongo
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


def make_exception_handler(status_code: int, message: str):
    def handler(_request: Request, _exc: Exception):
        return JSONResponse(status_code=status_code, content={"message": message})

    return handler


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        pymongo.errors.DuplicateKeyError,
        make_exception_handler(status.HTTP_409_CONFLICT, "This data already exists")
    )
