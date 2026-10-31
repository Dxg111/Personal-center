from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime
from app.database import get_session
from app.models import Project
from app.schemas import ProjectResponse, ProjectListResponse
import json

router = APIRouter(prefix="/api/projects", tags=["项目（公开）"])


@router.get("", response_model=List[ProjectListResponse])
def get_projects(
    category: Optional[str] = Query(None, pattern="^(project|work)$"),
    session: Session = Depends(get_session)
):
    """获取项目列表（访客端，仅返回已发布项目）"""
    # 公开接口不允许客户端决定是否包含草稿，始终只返回已发布项目
    statement = select(Project).where(Project.is_published == True)

    if category:
        statement = statement.where(Project.category == category)

    statement = statement.order_by(Project.sort_order, Project.created_at.desc())
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


@router.get("/featured", response_model=List[ProjectListResponse])
def get_featured_projects(
    limit: int = Query(3, ge=1, le=10),
    session: Session = Depends(get_session)
):
    """获取首页重点项目（前N个已发布项目，按 sort_order 排序）"""
    statement = (
        select(Project)
        .where(Project.is_published == True)
        .order_by(Project.sort_order, Project.created_at.desc())
        .limit(limit)
    )
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


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_detail(project_id: int, session: Session = Depends(get_session)):
    """获取项目详情（仅已发布项目，浏览量 +1）"""
    project = session.get(Project, project_id)
    # 未发布项目对访客视为不存在，避免通过 ID 直接访问草稿
    if not project or not project.is_published:
        raise HTTPException(status_code=404, detail="项目不存在")

    project.views_count += 1
    session.add(project)
    session.commit()
    session.refresh(project)

    # BUG-12 修复：解析项目图片JSON
    project_dict = project.model_dump()
    if project.project_images:
        try:
            project_dict['project_images'] = json.loads(project.project_images)
        except:
            project_dict['project_images'] = None

    return ProjectResponse(**project_dict)
