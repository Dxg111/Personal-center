# Personal Center

个人站 / 作品集，基于 Vue3 + FastAPI + MySQL，包含访客展示端和管理后台。

## 功能

**访客端**

- 首页 Hero、头像、简介、雷达技能、打字机文案
- 项目 / 作品分类切换
- 项目详情：Markdown、技术栈、外链、多图自动轮播、浏览量
- 404 页面、响应式布局、终端风格页脚

**管理端**

- JWT 登录与路由守卫
- 项目 CRUD、草稿 / 发布、多图上传、排序
- 个人信息、打字机文案、雷达技能编辑
- 管理员修改密码
- Markdown 实时预览

## 技术栈

| 层级 | 技术 |
|---|---|
| 前端 | Vue 3、Vite、Vue Router、Pinia、Tailwind CSS、marked、DOMPurify |
| 后端 | FastAPI、SQLModel、Pydantic、Uvicorn |
| 数据库 | MySQL 8 + Alembic |
| 测试 | pytest、Vitest、@vue/test-utils、jsdom |
| 部署 | Docker Compose、Nginx |

## 目录

```text
Personal-center/
├── backend/            # FastAPI + SQLModel + Alembic
│   ├── app/            # API、模型、schema、工具
│   ├── alembic/        # 数据库迁移
│   └── init_db.py      # 迁移 + 初始化管理员/个人信息
├── frontend/           # Vue3 + Vite
│   └── src/
│       ├── views/public/   # 首页、详情、404
│       └── views/admin/    # 登录、项目、个人信息、改密
├── docx/               # 需求、方案、部署指南
├── docker-compose.yml
└── docker-compose.env.example
```

## 本地开发

### 后端

```bash
cd backend

# 1. 创建数据库（Compose 部署会自动创建）
mysql -u root -p -e \
  "CREATE DATABASE personal_center CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. 配置环境变量
cp .env.example .env
# 编辑 DATABASE_URL、SECRET_KEY、ADMIN_PASSWORD

# 3. 安装依赖、迁移并初始化
pip install -r requirements.txt
python init_db.py

# 4. 启动
uvicorn app.main:app --reload --port 8000
```

- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

### 前端

```bash
cd frontend
npm install
npm run dev
```

- 前端：http://localhost:5173
- 管理后台：http://localhost:5173/admin/login

### Docker Compose

```bash
# 1. 准备环境变量
cp docker-compose.env.example .env
cp backend/.env.production.example backend/.env.production
# 编辑两处密码和 SECRET_KEY

# 2. 构建、迁移、启动
docker compose build
docker compose run --rm backend python init_db.py
docker compose up -d
```

- 前端：http://localhost:8080
- 管理后台：http://localhost:8080/admin/login
- 管理员密码：`backend/.env.production` 中的 `ADMIN_PASSWORD`

## 测试

```bash
# 后端
cd backend
python -m pytest test_main.py -q

# 前端
cd frontend
npm test
```

## 文档

- [需求分析](docx/需求分析文档.md)
- [方案设计](docx/方案设计文档.md)
- [VPS + Docker Compose 部署指南](docx/VPS-DockerCompose部署指南.md)
- [后端说明](backend/README.md)

## 安全提醒

- `.env`、`backend/.env.production` 已被 Git 忽略，不要提交
- 上线前修改 `SECRET_KEY` 和管理员密码
- 生产环境启用 HTTPS，只暴露 Nginx 的 80/443
- 定期备份 MySQL 和 `uploads` volume
