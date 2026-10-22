from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from datetime import datetime
from app.database import get_session
from app.models import AdminUser, Project, Profile
from app.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
    PublishToggle,
    ProfileResponse,
    ProfileUpdate,
)
from app.utils.auth import get_current_user
from app.utils.upload import save_upload_file

router = APIRouter(prefix="/api/admin", tags=["管理端"])


# ============ 项目管理 ============

@router.get("/projects", response_model=List[ProjectListResponse])
def get_admin_projects(
    session: Session = Depends(get_session),
    current_user: AdminUser = Depends(get_current_user)
):
    """获取后台项目列表（包含草稿）"""
    statement = select(Project).order_by(Project.created_at.desc())
    projects = session.exec(statement).all()
    return projects


@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_admin_project_detail(
    project_id: int,
    session: Session = Depends(get_session),
    current_user: AdminUser = Depends(get_current_user)
):
    """获取项目详情（管理端，不增加浏览量）- BUG-06 修复"""
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return db_project


@router.post("/projects", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: AdminUser = Depends(get_current_user)
):
    """新建项目"""
    db_project = Project(**project.model_dump())
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    session: Session = Depends(get_session),
    current_user: AdminUser = Depends(get_current_user)
):
    """编辑项目"""
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="项目不存在")

    # 更新字段
    for key, value in project.model_dump(exclude_unset=True).items():
        setattr(db_project, key, value)

    db_project.updated_at = datetime.utcnow()
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@router.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    session: Session = Depends(get_session),
    current_user: AdminUser = Depends(get_current_user)
):
    """删除项目"""
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="项目不存在")

    session.delete(db_project)
    session.commit()
    return {"message": "删除成功"}


@router.put("/projects/{project_id}/publish", response_model=ProjectResponse)
def toggle_publish(
    project_id: int,
    toggle: PublishToggle,
    session: Session = Depends(get_session),
    current_user: AdminUser = Depends(get_current_user)
):
    """切换项目发布状态"""
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="项目不存在")

    db_project.is_published = toggle.is_published
    db_project.updated_at = datetime.utcnow()
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


# ============ 个人信息管理 ============

@router.get("/profile", response_model=ProfileResponse)
def get_admin_profile(
    session: Session = Depends(get_session),
    current_user: AdminUser = Depends(get_current_user)
):
    """获取个人信息（管理端）"""
    statement = select(Profile).limit(1)
    profile = session.exec(statement).first()

    if not profile:
        raise HTTPException(status_code=404, detail="个人信息未配置")

    return profile


@router.put("/profile", response_model=ProfileResponse)
def update_profile(
    profile_data: ProfileUpdate,
    session: Session = Depends(get_session),
    current_user: AdminUser = Depends(get_current_user)
):
    """更新个人信息"""
    statement = select(Profile).limit(1)
    profile = session.exec(statement).first()

    if not profile:
        raise HTTPException(status_code=404, detail="个人信息未配置")

    # 更新字段
    for key, value in profile_data.model_dump().items():
        setattr(profile, key, value)

    profile.updated_at = datetime.utcnow()
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


# ============ 文件上传 ============

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: AdminUser = Depends(get_current_user)
):
    """上传图片（封面、头像等）"""
    url = await save_upload_file(file)
    return {"url": url}
