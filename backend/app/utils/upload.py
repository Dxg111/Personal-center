import os
import uuid
from typing import Optional

from fastapi import UploadFile, HTTPException

from app.config import get_settings

settings = get_settings()

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# 文件头签名 -> 规范扩展名；以实际内容为准，避免伪造扩展名
_IMAGE_SIGNATURES = (
    (b"\xff\xd8\xff", ".jpg"),
    (b"\x89PNG\r\n\x1a\n", ".png"),
)


def detect_image_extension(content: bytes) -> Optional[str]:
    """根据文件头识别真实图片类型，未知类型返回 None"""
    for signature, ext in _IMAGE_SIGNATURES:
        if content.startswith(signature):
            return ext

    # WebP: RIFF....WEBP
    if len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WEBP":
        return ".webp"

    return None


def validate_upload_file(file: UploadFile) -> None:
    """校验扩展名（真实内容校验在读取文件后进行）"""
    filename = file.filename or ""
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型。允许的类型：{', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )


async def save_upload_file(file: UploadFile, upload_dir: str = None) -> str:
    """保存上传文件并返回 URL"""
    if upload_dir is None:
        upload_dir = settings.UPLOAD_DIR

    # 先校验扩展名，再读取内容校验真实类型
    validate_upload_file(file)

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="上传文件为空")

    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制（最大 {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB）"
        )

    # 以文件头识别真实类型，防止把其他文件改名为 .jpg 上传
    ext = detect_image_extension(content)
    if ext is None:
        raise HTTPException(
            status_code=400,
            detail="文件内容不是有效的 JPG/PNG/WebP 图片"
        )

    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as f:
        f.write(content)

    # URL 与存储目录解耦，统一通过 /static/uploads/ 访问
    return f"/static/uploads/{filename}"
