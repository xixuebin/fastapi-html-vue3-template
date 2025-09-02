from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

# 模板目录仍为项目根下 offer_create/
templates = Jinja2Templates(directory="offer_create")
router = APIRouter()

# mock 数据
mock_offers = [
    {"title": "Offer A", "desc": "描述 A"},
    {"title": "Offer B", "desc": "描述 B"}
]

@router.get("/offer/create", response_class=HTMLResponse, operation_id="offer_create_page")
async def offer_create_page(request: Request):
    return templates.TemplateResponse("offer_create.html", {"request": request})

@router.post("/offer/create", response_class=HTMLResponse, operation_id="offer_create_submit")
async def offer_create_submit(request: Request, title: str = Form(...), desc: str = Form(...)):
    mock_offers.append({"title": title, "desc": desc})
    return RedirectResponse(url="/offer/list", status_code=status.HTTP_302_FOUND)

@router.get("/offer/list", response_class=HTMLResponse, operation_id="offer_list_page")
async def offer_list_page(request: Request):
    return templates.TemplateResponse("offer_list.html", {"request": request, "offers": mock_offers})

