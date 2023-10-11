from fastapi.routing import APIRouter

from app.rest.router_tags import RouterTags

router = APIRouter(prefix="/health", tags=[RouterTags.HEALTH])


@router.get("/")
def health():
    return {"status": "RUNNING"}
