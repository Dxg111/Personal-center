#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL数据库迁移脚本：添加雷达图技能和项目多图支持
BUG-11: 在 profile 表添加 radar_skills 字段
BUG-12: 在 project 表添加 project_images 字段
"""

import sys
import os
from pathlib import Path

# 设置输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加app目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def migrate():
    """执行数据库迁移"""
    if not DATABASE_URL:
        print("❌ 未找到 DATABASE_URL 配置")
        return False

    print(f"🔗 连接数据库: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'database'}")

    try:
        engine = create_engine(DATABASE_URL)
        inspector = inspect(engine)

        with engine.connect() as conn:
            # 检查 profile 表
            if 'profile' in inspector.get_table_names():
                profile_columns = [col['name'] for col in inspector.get_columns('profile')]

                if 'radar_skills' not in profile_columns:
                    print("⚙️  添加 profile.radar_skills 字段...")
                    conn.execute(text("ALTER TABLE profile ADD COLUMN radar_skills TEXT"))
                    conn.commit()
                    print("✅ profile.radar_skills 添加成功")
                else:
                    print("ℹ️  profile.radar_skills 字段已存在，跳过")
            else:
                print("⚠️  profile 表不存在")

            # 检查 project 表
            if 'project' in inspector.get_table_names():
                project_columns = [col['name'] for col in inspector.get_columns('project')]

                if 'project_images' not in project_columns:
                    print("⚙️  添加 project.project_images 字段...")
                    conn.execute(text("ALTER TABLE project ADD COLUMN project_images TEXT"))
                    conn.commit()
                    print("✅ project.project_images 添加成功")
                else:
                    print("ℹ️  project.project_images 字段已存在，跳过")
            else:
                print("⚠️  project 表不存在")

        print("\n🎉 数据库迁移完成！")
        return True

    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🔧 MySQL数据库迁移：添加雷达图和项目多图支持")
    print("=" * 60)
    print()

    success = migrate()

    if success:
        print("\n✨ 现在可以：")
        print("1. 在管理后台编辑个人信息，配置雷达图技能标签")
        print("2. 在编辑项目时，添加多张项目图片")
        print("3. 重启后端服务使更改生效")
    else:
        print("\n⚠️  迁移失败，请检查错误信息")
