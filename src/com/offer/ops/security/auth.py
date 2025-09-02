import os
from functools import wraps

from fastapi import Request, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
import yaml

# 从配置文件加载 API token
def load_api_token() -> str:
    config_path = "config.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config.get("api_token", "")
    return ""

API_TOKEN = load_api_token()

# API 密钥头部
api_key_header = APIKeyHeader(name="X-API-Token", auto_error=False)

# 登录校验装饰器
def requires_login(skip_login: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 如果标记为跳过登录校验，则直接执行函数
            if skip_login:
                return await func(*args, **kwargs)

            # 获取 request 对象
            request = kwargs.get('request')
            if not request:
                for arg in args:
                    if hasattr(arg, 'session'):
                        request = arg
                        break

            if not request or not hasattr(request, 'session'):
                raise HTTPException(status_code=401, detail="无法获取请求上下文")

            # 检查用户是否已登录
            username = request.session.get("user")
            if not username:
                raise HTTPException(status_code=401, detail="用户未登录")

            return await func(*args, **kwargs)
        return wrapper
    return decorator

# API token 校验装饰器（通过装饰器方式）
def requires_api_token():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取 request 对象
            request = kwargs.get('request')
            if not request:
                for arg in args:
                    if hasattr(arg, 'headers'):
                        request = arg
                        break

            # 从请求头获取 API token
            api_token = request.headers.get("X-API-Token")
            if not api_token:
                raise HTTPException(status_code=401, detail="缺少 API token")

            # 验证 API token
            if api_token != API_TOKEN:
                raise HTTPException(status_code=401, detail="API token 无效")

            return await func(*args, **kwargs)
        return wrapper
    return decorator

# 登录校验依赖（通过 Depends 方式）
async def verify_login(request: Request):
    username = request.session.get("user")
    if not username:
        raise HTTPException(status_code=401, detail="用户未登录")
    return username

# API token 校验依赖（通过 Depends 方式）
async def verify_api_token(x_api_token: str = Depends(api_key_header)):
    if not x_api_token:
        raise HTTPException(status_code=401, detail="缺少 API token")

    # 验证 API token
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="API token 无效")

    return x_api_token