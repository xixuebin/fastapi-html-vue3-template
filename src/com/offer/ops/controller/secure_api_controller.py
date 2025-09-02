from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from src.com.offer.ops.security.auth import verify_login, verify_api_token

router = APIRouter()

# 使用依赖注入方式进行登录校验的接口
@router.get("/api/secure/profile", response_class=JSONResponse)
async def secure_profile(request: Request, username: str = Depends(verify_login)):
    return {"message": f"用户 {username} 的安全信息", "data": {"level": "confidential"}}

# 使用依赖注入方式进行 API token 校验的接口
@router.get("/api/secure/data", response_class=JSONResponse)
async def secure_data(request: Request, api_token: str = Depends(verify_api_token)):
    return {"message": "受 API token 保护的安全数据", "data": {"encrypted": True}}