#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本：添加雷达图技能和项目多图支持
BUG-11: 在 profile 表添加 radar_skills 字段
BUG-12: 在 project 表添加 project_images 字段
"""

import sqlite3
import os
import sys
from pathlib import Path

# 设置输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 数据库路径
DB_PATH = Path(__file__).parent / "personal_center.db"


def migrate():
    """执行数据库迁移"""
    if not DB_PATH.exists():
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 检查 profile 表是否已有 radar_skills 字段
        cursor.execute("PRAGMA table_info(profile)")
        profile_columns = [col[1] for col in cursor.fetchall()]

        if 'radar_skills' not in profile_columns:
            print("⚙️  添加 profile.radar_skills 字段...")
            cursor.execute("ALTER TABLE profile ADD COLUMN radar_skills TEXT")
            print("✅ profile.radar_skills 添加成功")
        else:
            print("ℹ️  profile.radar_skills 字段已存在，跳过")

        # 检查 project 表是否已有 project_images 字段
        cursor.execute("PRAGMA table_info(project)")
        project_columns = [col[1] for col in cursor.fetchall()]

        if 'project_images' not in project_columns:
            print("⚙️  添加 project.project_images 字段...")
            cursor.execute("ALTER TABLE project ADD COLUMN project_images TEXT")
            print("✅ project.project_images 添加成功")
        else:
            print("ℹ️  project.project_images 字段已存在，跳过")

        conn.commit()
        print("\n🎉 数据库迁移完成！")
        return True

    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🔧 数据库迁移：添加雷达图和项目多图支持")
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
