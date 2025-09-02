from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.com.offer.ops.security.auth import requires_api_token, requires_login

router = APIRouter()

# 需要 API token 访问的公共接口
@router.get("/api/public/info", response_class=JSONResponse)
@requires_api_token()
async def public_info(request: Request):
    return {"message": "这是受 API token 保护的公共接口", "data": {"version": "1.0", "status": "active"}}

# 不需要登录校验的公开接口
@router.get("/api/public/status", response_class=JSONResponse)
@requires_login(skip_login=True)
async def public_status(request: Request):
    return {"status": "ok", "timestamp": "2023-01-01T00:00:00Z"}