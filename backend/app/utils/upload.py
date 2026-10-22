import os
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from app.config import get_settings

settings = get_settings()

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_upload_file(file: UploadFile) -> None:
    """验证上传文件"""
    # 检查文件扩展名
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型。允许的类型：{', '.join(ALLOWED_EXTENSIONS)}"
        )


async def save_upload_file(file: UploadFile, upload_dir: str = None) -> str:
    """保存上传文件并返回 URL"""
    if upload_dir is None:
        upload_dir = settings.UPLOAD_DIR

    # 验证文件
    validate_upload_file(file)

    # 确保上传目录存在
    os.makedirs(upload_dir, exist_ok=True)

    # 生成唯一文件名
    ext = os.path.splitext(file.filename)[1].lower()
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(upload_dir, filename)

    # 检查文件大小
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制（最大 {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB）"
        )

    # 保存文件
    with open(file_path, "wb") as f:
        f.write(content)

    # 返回相对 URL
    return f"/static/{settings.UPLOAD_DIR}/{filename}"
