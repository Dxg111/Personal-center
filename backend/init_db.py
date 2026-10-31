#!/usr/bin/env python3
"""
数据库初始化脚本
创建管理员账号 + 默认个人信息
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

# Windows 控制台默认可能是 GBK，统一改用 UTF-8 输出，避免 ✓ 等字符报错
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect
from sqlmodel import Session, select
from app.database import engine
from app.models import AdminUser, Profile
from app.utils.auth import get_password_hash
from app.config import get_settings

settings = get_settings()


def run_migrations():
    """执行 Alembic 迁移（兼容由 create_all 建表的旧数据库）"""
    alembic_cfg = Config(str(Path(__file__).resolve().parent / "alembic.ini"))

    tables = set(inspect(engine).get_table_names())
    legacy_tables = {"admin_user", "project", "profile"}

    # 旧库已有表但没有版本记录：先标记为当前最新版本，避免重复建表
    if "alembic_version" not in tables and legacy_tables.issubset(tables):
        print("检测到旧版数据库，正在标记迁移版本...")
        command.stamp(alembic_cfg, "head")

    command.upgrade(alembic_cfg, "head")


def init_database():
    """初始化数据库"""
    print("正在执行数据库迁移...")
    run_migrations()
    print("✓ 数据库迁移完成")

    with Session(engine) as session:
        # 1. 创建管理员账号
        statement = select(AdminUser).where(AdminUser.username == settings.ADMIN_USERNAME)
        existing_admin = session.exec(statement).first()

        if not existing_admin:
            admin = AdminUser(
                username=settings.ADMIN_USERNAME,
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD)
            )
            session.add(admin)
            session.commit()
            print(f"✓ 管理员账号创建成功：{settings.ADMIN_USERNAME}")
        else:
            print(f"✓ 管理员账号已存在：{settings.ADMIN_USERNAME}")

        # 2. 创建默认个人信息
        statement = select(Profile).limit(1)
        existing_profile = session.exec(statement).first()

        if not existing_profile:
            profile = Profile(
                name="YOUR NAME",
                avatar_url="/static/uploads/avatar-placeholder.jpg",
                bio="专注工业自动化、Python 工具链与全栈开发。做过轨道信号检测、列车平稳测试等工业项目。",
                typing_slogan="> 后端开发 · Python / FastAPI",
                wechat="your_wechat",
                email="hello@example.com",
                github_url="https://github.com/your-id"
            )
            session.add(profile)
            session.commit()
            print("✓ 默认个人信息创建成功")
        else:
            print("✓ 个人信息已存在")

    print("\n" + "="*50)
    print("数据库初始化完成！")
    print(f"管理员账号：{settings.ADMIN_USERNAME}")
    print(f"管理员密码：{settings.ADMIN_PASSWORD}")
    print("请通过后台管理界面修改个人信息")
    print("="*50)


if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"❌ 初始化失败：{e}")
        sys.exit(1)
