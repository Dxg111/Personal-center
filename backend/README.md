# Personal Center Backend

个人中心后端 API - 基于 FastAPI + SQLModel + MySQL

## 功能特性

- ✅ JWT 认证
- ✅ 项目 CRUD（支持草稿/发布）
- ✅ 个人信息管理
- ✅ 图片上传
- ✅ 自动生成 API 文档
- ✅ 完整单元测试

## 技术栈

- **框架**：FastAPI 0.115+
- **ORM**：SQLModel 0.0.22+
- **数据库**：MySQL 8.0+
- **认证**：JWT (python-jose + passlib)

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```ini
# 修改数据库密码
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/personal_center

# 生产环境请修改 SECRET_KEY
SECRET_KEY=your-secret-key-change-this-in-production-min-32-chars
```

### 3. 创建数据库

```sql
CREATE DATABASE personal_center CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 初始化数据库

```bash
python init_db.py
```

初始化完成后会显示：

```
管理员账号：admin
管理员密码：123456
```

### 5. 启动服务

```bash
uvicorn app.main:app --reload --port 8000
```

服务启动后访问：

- API 文档：http://localhost:8000/docs
- 接口测试：http://localhost:8000/redoc

## API 接口

### 公开接口（无需认证）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/profile` | 获取个人信息 |
| GET | `/api/projects` | 获取项目列表（支持 category 和 published 过滤） |
| GET | `/api/projects/featured` | 获取首页重点项目 |
| GET | `/api/projects/{id}` | 获取项目详情（浏览量 +1） |

### 认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/login` | 管理员登录（返回 JWT Token） |

### 管理接口（需要 JWT Token）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/admin/projects` | 获取后台项目列表（含草稿） |
| POST | `/api/admin/projects` | 新建项目 |
| PUT | `/api/admin/projects/{id}` | 编辑项目 |
| DELETE | `/api/admin/projects/{id}` | 删除项目 |
| PUT | `/api/admin/projects/{id}/publish` | 切换发布/草稿状态 |
| GET | `/api/admin/profile` | 获取个人信息 |
| PUT | `/api/admin/profile` | 更新个人信息 |
| POST | `/api/admin/upload` | 上传图片 |

## 运行测试

```bash
pytest test_main.py -v
```

## 项目结构

```
backend/
├── app/
│   ├── main.py           # FastAPI 应用入口
│   ├── config.py         # 配置管理
│   ├── database.py       # 数据库连接
│   ├── models/           # SQLModel 数据模型
│   ├── schemas/          # Pydantic 请求/响应模型
│   ├── api/              # API 路由
│   └── utils/            # 工具函数（认证、上传等）
├── uploads/              # 上传文件存储
├── init_db.py            # 数据库初始化脚本
├── test_main.py          # 单元测试
├── requirements.txt      # 依赖列表
└── .env                  # 环境变量（不提交 Git）
```

## 注意事项

1. **生产环境部署**：
   - 修改 `.env` 中的 `SECRET_KEY`（建议使用 `openssl rand -hex 32` 生成）
   - 修改 CORS 配置，只允许前端域名
   - 关闭数据库 `echo=True`
   - 使用 Gunicorn 或 Uvicorn workers

2. **图片上传**：
   - 当前存储在本地 `uploads/` 目录
   - 生产环境建议接入 OSS（阿里云/腾讯云）

3. **数据库备份**：
   - 定期备份 MySQL 数据库
   - 重要图片资源做异地备份

## License

MIT
