from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.api import auth, projects, profile, admin
import os

app = FastAPI(
    title="Personal Center API",
    description="个人中心后端 API",
    version="1.0.0"
)

# CORS 配置（开发环境允许所有来源，生产环境需要限制）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 前端开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务（上传的图片）
uploads_dir = "uploads"
if os.path.exists(uploads_dir):
    app.mount("/static/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# 注册路由
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(profile.router)
app.include_router(admin.router)


@app.on_event("startup")
async def on_startup():
    """启动时创建数据库表"""
    create_db_and_tables()


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
