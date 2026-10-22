from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Profile(SQLModel, table=True):
    """个人信息表（单行表）"""
    __tablename__ = "profile"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    avatar_url: str = Field(max_length=500)
    bio: str = Field(max_length=500)
    typing_slogan: str = Field(max_length=200)
    wechat: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=100)
    github_url: Optional[str] = Field(default=None, max_length=500)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
