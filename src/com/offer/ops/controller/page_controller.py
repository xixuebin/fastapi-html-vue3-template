from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from src.com.offer.ops.service import menu_service

router = APIRouter()

@router.get("/api/home", response_class=JSONResponse, operation_id="home_page")
async def home_page(request: Request):
    username = request.session.get("user")
    menus = menu_service.load_menus()
    return {"success": True, "username": username, "menus": menus}

@router.get("/api/welcome", response_class=JSONResponse, operation_id="welcome_page")
async def welcome_page(request: Request):
    username = request.session.get("user")
    return {"success": True, "username": username}

@router.get("/api/page1", response_class=JSONResponse, operation_id="page1")
async def page1(request: Request):
    username = request.session.get("user")
    return {"success": True, "username": username}

@router.get("/api/page2", response_class=JSONResponse, operation_id="page2")
async def page2(request: Request):
    username = request.session.get("user")
    return {"success": True, "username": username}
