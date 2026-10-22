from typing import Optional
from sqlmodel import SQLModel, Field, Column, Text
from datetime import datetime


class Project(SQLModel, table=True):
    """项目表"""
    __tablename__ = "project"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    summary: str = Field(max_length=500)
    content: str = Field(sa_column=Column(Text))
    cover_image: Optional[str] = Field(default=None, max_length=500)
    # BUG-12 修复：支持多张项目图片（JSON数组格式）
    project_images: Optional[str] = Field(default=None, sa_column=Column(Text))
    tech_stack: str = Field(default="", max_length=500)  # 逗号分隔
    demo_url: Optional[str] = Field(default=None, max_length=500)
    github_url: Optional[str] = Field(default=None, max_length=500)
    category: str = Field(default="project", max_length=50)  # project / work
    is_published: bool = Field(default=False)
    views_count: int = Field(default=0)
    sort_order: int = Field(default=999)  # 数字越小越靠前
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
