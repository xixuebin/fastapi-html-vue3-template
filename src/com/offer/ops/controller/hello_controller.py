from fastapi import APIRouter
from starlette import status
from starlette.responses import RedirectResponse

router = APIRouter()

@router.get("/", operation_id="hello_world")
async def root():
    return RedirectResponse(url="/index.html", status_code=status.HTTP_302_FOUND)

@router.get("/hello/{name}", operation_id="hello_name")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

