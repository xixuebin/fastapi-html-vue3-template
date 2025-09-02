from fastapi import APIRouter
from starlette import status
from starlette.responses import RedirectResponse

from com.offer.ops.security.auth import requires_login

router = APIRouter()

@router.get("/", operation_id="index")
async def root():
    if requires_login():
        return RedirectResponse(url="/login.html", status_code=status.HTTP_302_FOUND)
    return RedirectResponse(url="/index.html", status_code=status.HTTP_302_FOUND)

@router.get("/hello/{name}", operation_id="hello_name")
@requires_login(skip_login= True)
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

