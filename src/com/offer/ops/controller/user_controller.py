from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from src.com.offer.ops.service import user_service
from src.com.offer.ops.security.auth import requires_login

router = APIRouter()

# 登录接口不需要登录校验
@router.post("/api/login", response_class=JSONResponse, operation_id="login_submit")
@requires_login(skip_login=True)
async def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    if user_service.validate_user(username, password):
        request.session["user"] = username
        return {"success": True, "username": username}
    return {"success": False, "error": "用户名或密码错误"}

# 登出接口需要登录校验
@router.post("/api/logout", response_class=JSONResponse, operation_id="logout")
@requires_login()
async def logout(request: Request):
    request.session.clear()
    return {"success": True}