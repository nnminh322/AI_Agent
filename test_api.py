from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, FileResponse
from loguru import logger
import os
from functional import chat_sql

app = FastAPI(
    title="Data Agent",
    description="copyright: nnminh322@gmail.com",
    version="1.0.0 beta"
)

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    """
    Endpoint này phục vụ file index.html làm giao diện người dùng.
    Nó giải quyết lỗi 404 khi truy cập vào trang gốc.
    """
    try:
        with open("app/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Lỗi: Không tìm thấy file index.html</h1>", status_code=404)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Endpoint này phục vụ file icon cho trang web.
    Nó giải quyết lỗi 404 cho file favicon.ico.
    """
    favicon_path = "app/icon_chat.ico"
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    return FileResponse(None, status_code=404)

@app.post("/chat")
async def chat(text: str):
    """
    Endpoint chính để xử lý yêu cầu chat từ người dùng.
    """
    logger.info(f"User: {text}")
    response = chat_sql(question=text)
    return {"response": response["results"]}


