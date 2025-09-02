from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

class AuthenticatedStaticFiles(BaseHTTPMiddleware):
    def __init__(self, app, static_dir: str, login_url: str = "/static/login.html",
                 public_paths: set = None, **kwargs):
        super().__init__(app)
        self.static_dir = static_dir
        self.login_url = login_url
        # 默认情况下，登录页面和静态资源无需登录即可访问
        self.public_paths = public_paths or {
            "/static/login.html",
            "/static/style.css",
            # 可以添加其他不需要登录验证的静态资源路径
        }

    async def dispatch(self, request: Request, call_next):
        # 如果不是对静态文件的请求，继续处理
        path = request.url.path
        if not (path == "/" or path.startswith("/static/") or path.endswith(".html")):
            return await call_next(request)

        # 处理根路径请求，重定向到 index.html
        if path == "/":
            path = "/static/index.html"

        # 检查是否为不需要登录验证的路径
        if path in self.public_paths or any(path.endswith(ext) for ext in [".css", ".js", ".ico", ".png", ".jpg", ".jpeg", ".gif"]):
            return await call_next(request)

        # 检查用户是否已登录
        username = request.session.get("user")
        if not username:
            # 用户未登录，重定向到登录页面
            return RedirectResponse(url=self.login_url)

        # 用户已登录，继续处理请求
        return await call_next(request)
