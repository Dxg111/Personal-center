from sqlmodel import SQLModel, create_engine, Session
from app.config import get_settings

settings = get_settings()

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQL_ECHO,  # 通过 SQL_ECHO 环境变量控制，生产默认关闭
    pool_pre_ping=True,  # 自动重连
)


def create_db_and_tables():
    """创建所有表"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """获取数据库会话（依赖注入）"""
    with Session(engine) as session:
        yield session
