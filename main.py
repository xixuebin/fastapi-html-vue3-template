from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_mcp import FastApiMCP
from starlette.middleware.sessions import SessionMiddleware

from src.com.offer.ops.controller.user_controller import router as user_router
from src.com.offer.ops.controller.page_controller import router as page_router
from src.com.offer.ops.controller.hello_controller import router as hello_router
from src.com.offer.ops.controller.offer_create_controller import router as offer_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

# 先包含所有API路由
app.include_router(user_router)
app.include_router(page_router)
app.include_router(hello_router)
app.include_router(offer_router)

# 将静态文件挂载放在最后，避免影响API路由
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", StaticFiles(directory="static", html=True), name="root")

mcp_app = FastApiMCP(app)
mcp_app.mount_http()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)