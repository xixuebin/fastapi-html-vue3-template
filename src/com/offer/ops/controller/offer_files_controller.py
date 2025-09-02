import os
import time
from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel

from src.com.offer.ops.security.auth import requires_login

# 定义上传文件夹和允许的文件扩展名
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../../uploads")
ALLOWED_EXTENSIONS = {"csv"}

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

# 文件列表 API - 从 requires_api_token 改为 requires_login
@router.get("/api/files", response_class=JSONResponse, operation_id="list_files")
@requires_login()  # 修改这里，允许已登录用户访问
async def list_files(request: Request):
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
async def upload_file(request: Request,file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="没有文件上传")

    filename = file.filename
    if not allowed_file(filename):
        raise HTTPException(status_code=400, detail="不允许的文件类型")

    # 保存文件
    timestamp = int(time.time())
    new_filename = f"{os.path.splitext(filename)[0]}-{timestamp}{os.path.splitext(filename)[1]}"
    file_path = os.path.join(UPLOAD_FOLDER, new_filename)
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
async def download_file(request: Request,filename: str):
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
@requires_login()
async def delete_file(request: Request, filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    try:
        os.remove(file_path)
        return {"success": True, "message": "文件删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文件失败：{str(e)}")



@router.get('/api/files/view/<path:filename>', response_class=HTMLResponse, operation_id="view_file")
@requires_login()
def view_file(request: Request, filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.isfile(file_path):
        return HTTPException(status_code=404, detail="文件不存在")
    def generate():
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            yield '<!DOCTYPE html><html><head><meta charset="utf-8"><title>{}</title><style>body{{font-family:monospace;white-space:pre-wrap;word-break:break-all;background:#f8f8f8;margin:0;padding:20px;}}</style></head><body><h2>{}</h2><hr><pre>'.format(filename, filename)
            header = None
            for line in f:
                fields = [cell.replace('<', '&lt;').replace('>', '&gt;').strip() for cell in line.strip().split(',')]
                if header is None:
                    header = fields
                    yield '<table border="1" cellpadding="5" cellspacing="0"><thead><tr>' + ''.join(
                        f'<th>{h}</th>' for h in header) + '</tr></thead><tbody>'
                else:
                    yield '<tr>' + ''.join(f'<td>{cell}</td>' for cell in fields) + '</tr>'
            yield '</tbody></table>'
            yield '</pre></body></html>'
    return HTMLResponse(generate())