from fastapi.routing import APIRouter

from app.rest.router_tags import RouterTags

router = APIRouter(prefix="/card", tags=[RouterTags.CARD])


@router.post("/", status_code=422)
def create_card():
    return {}
