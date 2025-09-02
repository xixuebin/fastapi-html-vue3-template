from fastapi import APIRouter, Request
from starlette import status
from starlette.responses import RedirectResponse

from com.offer.ops.security.auth import requires_login

router = APIRouter()

@router.get("/", operation_id="index")
async def root(request: Request):
    # 检查用户是否已登录
    username = request.session.get("user")
    if not username:
        # 未登录，重定向到登录页面
        return RedirectResponse(url="/static/login.html", status_code=status.HTTP_302_FOUND)
    # 已登录，重定向到主页
    return RedirectResponse(url="/static/index.html", status_code=status.HTTP_302_FOUND)

@router.get("/hello/{name}", operation_id="hello_name")
@requires_login()  # 移除 skip_login=True，启用登录验证
async def say_hello(name: str):
    return {"message": f"Hello {name}"}