from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class AdminUser(SQLModel, table=True):
    """管理员用户表"""
    __tablename__ = "admin_user"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
