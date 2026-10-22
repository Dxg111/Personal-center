from typing import Optional
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    token_type: str = "bearer"


class ProfileResponse(BaseModel):
    """个人信息响应"""
    id: int
    name: str
    avatar_url: str
    bio: str
    typing_slogan: str
    wechat: Optional[str] = None
    email: Optional[str] = None
    github_url: Optional[str] = None


class ProfileUpdate(BaseModel):
    """更新个人信息"""
    name: str = Field(min_length=1, max_length=100)
    avatar_url: str = Field(max_length=500)
    bio: str = Field(max_length=500)
    typing_slogan: str = Field(max_length=200)
    wechat: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=100)
    github_url: Optional[str] = Field(default=None, max_length=500)
