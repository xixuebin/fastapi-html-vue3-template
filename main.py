from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_mcp import FastApiMCP
from fastapi.templating import Jinja2Templates
import yaml
from starlette.middleware.sessions import SessionMiddleware
from com.offer.ops.offer_create import router as offer_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 读取用户配置
def load_users():
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config.get("users", [])

users = load_users()

def load_menus():
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config.get("menus", [])

menus = load_menus()

mcp_app = FastApiMCP(app)
mcp_app.mount_http()

app.include_router(offer_router)

@app.get("/login", response_class=HTMLResponse, operation_id="login_page")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login", response_class=HTMLResponse, operation_id="login_submit")
async def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    for user in users:
        if user["username"] == username and user["password"] == password:
            request.session["user"] = username
            return RedirectResponse(url="/home", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("login.html", {"request": request, "error": "用户名或密码错误"})

@app.get("/home", response_class=HTMLResponse, operation_id="home_page")
async def home_page(request: Request):
    username = request.session.get("user")
    if not username:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("home.html", {"request": request, "username": username, "menus": menus})


@app.get("/welcome", response_class=HTMLResponse, operation_id="home_page")
async def home_page(request: Request):
    username = request.session.get("user")
    if not username:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("welcome.html", {"request": request, "username": username})

@app.get("/logout", operation_id="logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@app.get("/", operation_id="hello_world")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}", operation_id="hello_name")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/page1", response_class=HTMLResponse, operation_id="page1")
async def page1(request: Request):
    username = request.session.get("user")
    if not username:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("page1.html", {"request": request, "username": username})

@app.get("/page2", response_class=HTMLResponse, operation_id="page2")
async def page2(request: Request):
    username = request.session.get("user")
    if not username:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("page2.html", {"request": request, "username": username})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
