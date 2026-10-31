import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api import auth, projects, profile, admin

settings = get_settings()

# 数据表由 Alembic 迁移管理（init_db.py 会自动执行 upgrade head）
app = FastAPI(
    title="Personal Center API",
    description="个人中心后端 API",
    version="1.0.0",
)

# CORS 配置（通过 CORS_ORIGINS 环境变量配置，多个用逗号分隔）
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务（上传的图片）；启动时确保目录存在，避免目录缺失导致挂载失效
uploads_dir = settings.UPLOAD_DIR
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# 注册路由
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(profile.router)
app.include_router(admin.router)


@app.get("/")
def read_root():
    """根路径"""
    return {
        "message": "Personal Center API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "ok"}
