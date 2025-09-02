from fastapi import APIRouter

router = APIRouter()

@router.get("/", operation_id="hello_world")
async def root():
    return {"message": "Hello World"}

@router.get("/hello/{name}", operation_id="hello_name")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

