from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class ProjectBase(BaseModel):
    """项目基础字段（除发布时的标题外，其余均可留空）"""
    title: str = Field(default="", max_length=200)
    summary: str = Field(default="", max_length=500)
    content: str = ""
    cover_image: Optional[str] = Field(default=None, max_length=500)
    # BUG-12 修复：支持多张项目图片
    project_images: Optional[List[str]] = None
    tech_stack: str = Field(default="", max_length=500)
    demo_url: Optional[str] = Field(default=None, max_length=500)
    github_url: Optional[str] = Field(default=None, max_length=500)
    category: str = Field(default="project", pattern="^(project|work)$")
    sort_order: int = Field(default=999, ge=0)


class ProjectCreate(ProjectBase):
    """创建项目"""
    is_published: bool = Field(default=False)


class ProjectUpdate(ProjectBase):
    """更新项目"""
    is_published: Optional[bool] = None


class ProjectResponse(ProjectBase):
    """项目响应"""
    id: int
    is_published: bool
    views_count: int
    created_at: datetime
    updated_at: datetime


class ProjectListResponse(BaseModel):
    """项目列表响应"""
    id: int
    title: str
    summary: str
    cover_image: Optional[str]
    # BUG-12 修复：支持多张项目图片
    project_images: Optional[List[str]]
    tech_stack: str
    category: str
    is_published: bool
    views_count: int
    created_at: datetime


class PublishToggle(BaseModel):
    """切换发布状态"""
    is_published: bool
