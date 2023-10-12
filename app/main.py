from fastapi import FastAPI
from starlette import status
from starlette.responses import RedirectResponse

from app.rest import register_routers

app = FastAPI()

register_routers(app)


@app.get("/", response_class=RedirectResponse, status_code=status.HTTP_308_PERMANENT_REDIRECT)
def redirect_to_docs():
    return "/docs"  # pragma: no cover
