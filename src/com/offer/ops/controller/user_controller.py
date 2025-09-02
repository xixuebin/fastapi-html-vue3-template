from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse, JSONResponse
from src.com.offer.ops.service import user_service

router = APIRouter()

@router.post("/api/login", response_class=JSONResponse, operation_id="login_submit")
async def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    if user_service.validate_user(username, password):
        request.session["user"] = username
        return {"success": True, "username": username}
    return {"success": False, "error": "用户名或密码错误"}

@router.post("/api/logout", response_class=JSONResponse, operation_id="logout")
async def logout(request: Request):
    request.session.clear()
    return {"success": True}
