from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse

from com.offer.ops.security.auth import requires_login

router = APIRouter()

# mock 数据
mock_offers = [
    {"title": "Offer A", "desc": "描述 A"},
    {"title": "Offer B", "desc": "描述 B"}
]

@router.post("/offer/create", response_class=HTMLResponse, operation_id="offer_create_submit")
@requires_login()
async def offer_create_submit(request: Request, title: str = Form(...), desc: str = Form(...)):
    mock_offers.append({"title": title, "desc": desc})
    return RedirectResponse(url="/offer/list", status_code=status.HTTP_302_FOUND)

@router.get("/api/offer/list", response_class=JSONResponse, operation_id="offer_list_api")
@requires_login()
async def offer_list_api():
    return {"offers": mock_offers}
