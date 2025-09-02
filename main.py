from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_mcp import FastApiMCP
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates

from src.com.offer.ops.controller.user_controller import router as user_router
from src.com.offer.ops.controller.page_controller import router as page_router
from src.com.offer.ops.controller.hello_controller import router as hello_router
from com.offer.ops.offer_create import router as offer_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

mcp_app = FastApiMCP(app)
mcp_app.mount_http()

app.include_router(user_router)
app.include_router(page_router)
app.include_router(hello_router)
app.include_router(offer_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
