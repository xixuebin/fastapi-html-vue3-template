import os
import time
from typing import List
from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.com.offer.ops.security.auth import requires_login, requires_api_token

# 定义上传文件夹和允许的文件扩展名
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "doc", "docx", "xls", "xlsx"}

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

router = APIRouter()

# 文件信息模型
class FileInfo(BaseModel):
    name: str
    size: int
    modified: str
    path: str

def allowed_file(filename: str) -> bool:
    """检查文件名是否有允许的扩展名"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 文件管理页面
@router.get("/files", response_class=HTMLResponse, operation_id="files_page")
@requires_login()
async def files_page(request: Request):
    return HTMLResponse(content=open("static/offer/files.html").read())

# 文件列表 API
@router.get("/api/files", response_class=JSONResponse, operation_id="list_files")
@requires_api_token()
async def list_files():
    files = []
    for name in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, name)
        if os.path.isfile(path):
            files.append(FileInfo(
                name=name,
                size=os.path.getsize(path),
                modified=time.ctime(os.path.getmtime(path)),
                path=f"/files/download/{name}"
            ))
    return {"files": [file.dict() for file in files]}

# 文件上传 API
@router.post("/api/files/upload", response_class=JSONResponse, operation_id="upload_file")
@requires_login()
async def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="没有文件上传")

    filename = file.filename
    if not allowed_file(filename):
        raise HTTPException(status_code=400, detail="不允许的文件类型")

    # 保存文件
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "success": True,
        "filename": filename,
        "message": "文件上传成功"
    }

# 文件下载 API
@router.get("/files/download/{filename}", operation_id="download_file")
@requires_login()
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )

# 删除文件 API
@router.delete("/api/files/{filename}", response_class=JSONResponse, operation_id="delete_file")
@requires_api_token()
async def delete_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    try:
        os.remove(file_path)
        return {"success": True, "message": "文件删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文件失败：{str(e)}")
