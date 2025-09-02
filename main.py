from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_mcp import FastApiMCP
from starlette.middleware.sessions import SessionMiddleware

from src.com.offer.ops.controller.auth_controller import router as user_router
from src.com.offer.ops.controller.page_controller import router as page_router
from src.com.offer.ops.controller.hello_controller import router as hello_router
from src.com.offer.ops.controller.offer_create_controller import router as offer_router
from src.com.offer.ops.controller.public_api_controller import router as public_api_router
from src.com.offer.ops.controller.secure_api_controller import router as secure_api_router
from src.com.offer.ops.middleware.static_middleware import AuthenticatedStaticFiles
from src.com.offer.ops.controller.offer_files_controller import router as files_router

app = FastAPI()

# 先包含所有 API 路由
app.include_router(user_router)
app.include_router(page_router)
app.include_router(hello_router)
app.include_router(offer_router)
app.include_router(public_api_router)
app.include_router(secure_api_router)

app.include_router(files_router)

# 将静态文件挂载放在最后，避免影响 API 路由
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", StaticFiles(directory="static", html=True), name="root")

# 中间件添加顺序很重要，它们会按照相反的顺序执行
# 先添加自定义静态文件中间件，确保它在会话中间件之后执行
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

# 最后添加会话中间件，确保它最先执行
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

mcp_app = FastApiMCP(app)
mcp_app.mount_http()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)