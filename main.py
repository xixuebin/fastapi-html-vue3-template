from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_mcp import FastApiMCP
from starlette.middleware.sessions import SessionMiddleware

from src.com.offer.ops.controller.user_controller import router as user_router
from src.com.offer.ops.controller.page_controller import router as page_router
from src.com.offer.ops.controller.hello_controller import router as hello_router
from src.com.offer.ops.controller.offer_create_controller import router as offer_router
from src.com.offer.ops.controller.public_api_controller import router as public_api_router
from src.com.offer.ops.controller.secure_api_controller import router as secure_api_router
from src.com.offer.ops.middleware.static_middleware import AuthenticatedStaticFiles

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
# 添加认证静态文件中间件，在 session 中间件之后添加
app.add_middleware(
    AuthenticatedStaticFiles,
    static_dir="static",
    login_url="/static/login.html",
    public_paths={
        "/static/login.html",
        "/static/style.css",
        # 可以添加其他无需登录即可访问的路径
    }
)

# 先包含所有 API 路由
app.include_router(user_router)
app.include_router(page_router)
app.include_router(hello_router)
app.include_router(offer_router)
app.include_router(public_api_router)
app.include_router(secure_api_router)

# 将静态文件挂载放在最后，避免影响 API 路由
# app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", StaticFiles(directory="static", html=True), name="root")

mcp_app = FastApiMCP(app)
mcp_app.mount_http()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)