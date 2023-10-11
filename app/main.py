from fastapi import FastAPI
from starlette import status
from starlette.responses import RedirectResponse

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "RUNNING"}


@app.get("/", response_class=RedirectResponse, status_code=status.HTTP_308_PERMANENT_REDIRECT)
def root():
    return "/docs"  # pragma: no cover
