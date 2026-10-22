import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

# 从 .env 读取配置
db_url = os.getenv("DATABASE_URL")
print(f"数据库 URL: {db_url}")

# 解析连接信息
if db_url:
    # 格式: mysql+pymysql://root:password@localhost:3306/personal_center
    parts = db_url.replace("mysql+pymysql://", "").split("@")
    user_pass = parts[0].split(":")
    host_db = parts[1].split("/")
    host_port = host_db[0].split(":")

    user = user_pass[0]
    password = user_pass[1] if len(user_pass) > 1 else ""
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else 3306
    database = host_db[1] if len(host_db) > 1 else ""

    print(f"\n连接信息：")
    print(f"  用户: {user}")
    print(f"  密码: {'*' * len(password)}")
    print(f"  主机: {host}")
    print(f"  端口: {port}")
    print(f"  数据库: {database}")

    try:
        # 先测试连接 MySQL（不指定数据库）
        print(f"\n正在测试 MySQL 连接...")
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        print("✓ MySQL 连接成功")

        # 检查数据库是否存在
        cursor = conn.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{database}'")
        result = cursor.fetchone()

        if result:
            print(f"✓ 数据库 '{database}' 已存在")
        else:
            print(f"✗ 数据库 '{database}' 不存在")
            print(f"\n请手动创建数据库：")
            print(f"  CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"✗ 连接失败: {e}")
        print("\n请检查：")
        print("1. MySQL 服务是否启动")
        print("2. 用户名和密码是否正确")
        print("3. .env 文件中的 DATABASE_URL 配置")
else:
    print("错误：未找到 DATABASE_URL 配置")
