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
import json

router = APIRouter(prefix="/api/admin", tags=["管理端"])


def ensure_publishable(project: Project) -> None:
    """发布的项目至少需要有标题，草稿允许部分内容为空"""
    if project.is_published and not project.title.strip():
        raise HTTPException(status_code=422, detail="发布项目前请填写标题")


# ============ 项目管理 ============

@router.get("/projects", response_model=List[ProjectListResponse])
def get_admin_projects(
    session: Session = Depends(get_session),
    current_user: AdminUser = Depends(get_current_user)
):
    """获取后台项目列表（包含草稿）"""
    statement = select(Project).order_by(Project.created_at.desc())
    projects = session.exec(statement).all()

    # BUG-12 修复：解析项目图片JSON
    result = []
    for project in projects:
        project_dict = project.model_dump()
        if project.project_images:
            try:
                project_dict['project_images'] = json.loads(project.project_images)
            except:
                project_dict['project_images'] = None
        result.append(ProjectListResponse(**project_dict))

    return result


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

    # BUG-12 修复：解析项目图片JSON
    project_dict = db_project.model_dump()
    if db_project.project_images:
        try:
            project_dict['project_images'] = json.loads(db_project.project_images)
        except:
            project_dict['project_images'] = None

    return ProjectResponse(**project_dict)


@router.post("/projects", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: AdminUser = Depends(get_current_user)
):
    """新建项目"""
    project_data = project.model_dump()

    # BUG-12 修复：将项目图片列表转换为JSON字符串存储
    if project_data.get('project_images'):
        project_data['project_images'] = json.dumps(project_data['project_images'])

    db_project = Project(**project_data)
    db_project.title = db_project.title.strip()
    ensure_publishable(db_project)

    session.add(db_project)
    session.commit()
    session.refresh(db_project)

    # BUG-12 修复：返回时解析JSON
    project_dict = db_project.model_dump()
    if db_project.project_images:
        try:
            project_dict['project_images'] = json.loads(db_project.project_images)
        except:
            project_dict['project_images'] = None

    return ProjectResponse(**project_dict)


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
    project_data = project.model_dump(exclude_unset=True)

    # BUG-12 修复：将项目图片列表转换为JSON字符串存储
    if 'project_images' in project_data and project_data['project_images'] is not None:
        project_data['project_images'] = json.dumps(project_data['project_images'])

    for key, value in project_data.items():
        setattr(db_project, key, value)

    db_project.title = db_project.title.strip()
    db_project.updated_at = datetime.utcnow()
    ensure_publishable(db_project)

    session.add(db_project)
    session.commit()
    session.refresh(db_project)

    # BUG-12 修复：返回时解析JSON
    project_dict = db_project.model_dump()
    if db_project.project_images:
        try:
            project_dict['project_images'] = json.loads(db_project.project_images)
        except:
            project_dict['project_images'] = None

    return ProjectResponse(**project_dict)


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
    ensure_publishable(db_project)

    session.add(db_project)
    session.commit()
    session.refresh(db_project)

    # BUG-12 修复：返回时解析JSON
    project_dict = db_project.model_dump()
    if db_project.project_images:
        try:
            project_dict['project_images'] = json.loads(db_project.project_images)
        except:
            project_dict['project_images'] = None

    return ProjectResponse(**project_dict)


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

    # BUG-11 修复：解析雷达图技能JSON
    profile_dict = profile.model_dump()
    if profile.radar_skills:
        try:
            profile_dict['radar_skills'] = json.loads(profile.radar_skills)
        except:
            profile_dict['radar_skills'] = None

    return ProfileResponse(**profile_dict)


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
    update_data = profile_data.model_dump()

    # BUG-11 修复：将雷达图技能列表转换为JSON字符串存储
    if 'radar_skills' in update_data and update_data['radar_skills'] is not None:
        update_data['radar_skills'] = json.dumps([skill.dict() for skill in profile_data.radar_skills])

    for key, value in update_data.items():
        setattr(profile, key, value)

    profile.updated_at = datetime.utcnow()
    session.add(profile)
    session.commit()
    session.refresh(profile)

    # BUG-11 修复：返回时解析JSON
    profile_dict = profile.model_dump()
    if profile.radar_skills:
        try:
            profile_dict['radar_skills'] = json.loads(profile.radar_skills)
        except:
            profile_dict['radar_skills'] = None

    return ProfileResponse(**profile_dict)


# ============ 文件上传 ============

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: AdminUser = Depends(get_current_user)
):
    """上传图片（封面、头像等）"""
    url = await save_upload_file(file)
    return {"url": url}
