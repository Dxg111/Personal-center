from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend 目录，确保无论从哪个工作目录启动都能找到 .env
BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """应用配置"""
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "123456"
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 5242880  # 5MB

    # 开发环境可开启 SQL 日志；生产环境默认关闭
    SQL_ECHO: bool = False
    # 允许跨域的前端地址，多个用逗号分隔
    CORS_ORIGINS: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"), extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        """将逗号分隔的跨域配置解析为列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache()
def get_settings():
    return Settings()
