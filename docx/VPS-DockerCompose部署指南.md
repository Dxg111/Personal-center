# Personal Center 单台 VPS + Docker Compose 部署指南

> 版本：v1.0  
> 日期：2026-11-01  
> 适用：个人站、低流量生产环境、本地 Docker Desktop 验证  
> 技术栈：Vue3 + Vite / FastAPI + SQLModel / MySQL 8 / Nginx / Docker Compose

---

## 一、方案概览

### 1.1 架构

```text
                    Internet
                       │
                 80 / 443
                       │
        ┌──────────────▼──────────────┐
        │  frontend（Nginx）           │
        │  ├─ /         → dist 静态文件 │
        │  ├─ /api/     → backend:8000 │
        │  └─ /static/  → backend:8000 │
        └──────────────┬──────────────┘
                       │ Docker 内部网络 appnet
        ┌──────────────▼──────────────┐
        │  backend（FastAPI + Uvicorn）│
        │  监听 8000，不对公网暴露      │
        └──────────────┬──────────────┘
                       │ mysql:3306
        ┌──────────────▼──────────────┐
        │  mysql（MySQL 8.0）          │
        └──────────────┬──────────────┘
                       │
              named volume（持久化）
```

### 1.2 容器与端口

| 服务 | 镜像/构建 | 对宿主机暴露 | 说明 |
|---|---|---|---|
| frontend | `frontend/Dockerfile` | `FRONTEND_PORT:80` | 唯一对公网开放 |
| backend | `backend/Dockerfile` | 不暴露 | 仅 Docker 内网访问 |
| mysql | `mysql:8.0` | 不暴露 | 仅 Docker 内网访问 |

### 1.3 数据持久化

| 数据 | 容器路径 | 存储 |
|---|---|---|
| MySQL 数据 | `/var/lib/mysql` | named volume `mysql_data` |
| 上传图片 | `/app/uploads` | named volume `uploads_data` |

> 容器可以随时重建，volume 必须单独备份。

---

## 二、仓库中的部署文件

```text
Personal-center/
├── docker-compose.yml                 # Compose 编排
├── docker-compose.env.example         # Compose 变量示例
├── .env                               # 本地生成，已被 git 忽略
├── backend/
│   ├── Dockerfile                     # Python 3.11 + Uvicorn
│   ├── .dockerignore
│   ├── .env.production                # 本地生成，已被 git 忽略
│   └── .env.production.example        # 生产配置示例
└── frontend/
    ├── Dockerfile                     # Node 22 构建 → Nginx
    ├── nginx.conf
    └── .dockerignore
```

本地已生成：

- `.env`：Compose 变量（MySQL 密码、端口、CORS 地址）
- `backend/.env.production`：后端密钥和管理员密码

这两个文件都已被 `.gitignore` 忽略，不会进入 Git，也不会被复制进镜像。

---

## 三、本地快速验证（Windows + Docker Desktop）

### 3.1 前置条件

- Docker Desktop 已安装并启动
- 可用内存建议 ≥ 2GB（构建 + MySQL + 后端）
- 本地端口 `8080` 未被占用

### 3.2 启动流程

```bash
cd /path/to/Personal-center

# 1. 校验 Compose 配置
docker compose config --quiet

# 2. 构建镜像
docker compose build

# 3. 执行数据库迁移 + 初始化管理员/个人信息
docker compose run --rm backend python init_db.py

# 4. 启动全部服务
docker compose up -d

# 5. 查看状态
docker compose ps
```

### 3.3 访问地址

- 前端：http://localhost:8080
- 管理后台：http://localhost:8080/admin/login
- 用户名：`admin`
- 密码：查看 `backend/.env.production` 中的 `ADMIN_PASSWORD`
- 后端健康检查（容器内）：`http://localhost:8000/health`

### 3.4 常用命令

```bash
# 查看日志
docker compose logs -f --tail=200 backend
docker compose logs -f --tail=200 frontend
docker compose logs -f --tail=200 mysql

# 重启单个服务
docker compose restart backend

# 停止（保留数据）
docker compose down

# 停止并删除数据卷（危险：数据库和图片全部删除）
docker compose down -v
```

---

## 四、环境变量

### 4.1 根目录 `.env`（Compose 变量）

| 变量 | 说明 | 本地示例 |
|---|---|---|
| `MYSQL_ROOT_PASSWORD` | MySQL root 密码 | 随机生成 |
| `MYSQL_DATABASE` | 数据库名 | `personal_center` |
| `MYSQL_USER` | 应用数据库用户 | `pcenter` |
| `MYSQL_PASSWORD` | 应用数据库密码 | 随机生成 |
| `PUBLIC_ORIGIN` | 站点对外地址，用于 CORS | `http://localhost:8080` |
| `FRONTEND_PORT` | 前端映射到宿主机的端口 | 本地 `8080`，生产 `80` |
| `NPM_REGISTRY` | 前端构建使用的 npm 源 | 国内可用 `https://registry.npmmirror.com`，默认官方源 |

### 4.2 `backend/.env.production`（应用配置）

| 变量 | 说明 |
|---|---|
| `SECRET_KEY` | JWT 签名密钥，必须为强随机值 |
| `ALGORITHM` | 默认 `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token 有效期，默认 1440 分钟 |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | 初始化管理员账号 |
| `UPLOAD_DIR` | 上传目录，容器内为 `/app/uploads` |
| `MAX_UPLOAD_SIZE` | 单文件大小限制，默认 5MB |
| `SQL_ECHO` | 是否打印 SQL，生产必须 `false` |
| `CORS_ORIGINS` | 允许的前端来源，多个用逗号分隔 |

Compose 会覆盖以下变量，避免把数据库地址写死：

- `DATABASE_URL` → `mysql+pymysql://...@mysql:3306/personal_center`
- `UPLOAD_DIR` → `/app/uploads`
- `SQL_ECHO` → `false`
- `CORS_ORIGINS` → `${PUBLIC_ORIGIN}`

---

## 五、Compose 关键设计

### 5.1 MySQL 健康检查

```yaml
healthcheck:
  test: ["CMD-SHELL", "mysqladmin ping -h 127.0.0.1 -u$$MYSQL_USER -p$$MYSQL_PASSWORD --silent"]
  interval: 10s
  timeout: 5s
  retries: 10
  start_period: 30s
```

`$$` 用于转义 Compose 插值，让变量在容器内部展开。

### 5.2 后端等待 MySQL 就绪

```yaml
depends_on:
  mysql:
    condition: service_healthy
```

只写 `depends_on: [mysql]` 只能保证启动顺序，不能保证 MySQL 已经可连接。

### 5.3 后端健康检查

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
```

使用 `/health` 而不是 `/api/profile`：前者不依赖数据库和种子数据，首次迁移前不会误判 unhealthy。

### 5.4 日志轮转

```yaml
logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```

避免容器日志无限增长写满磁盘。

---

## 六、Nginx 配置要点

`frontend/nginx.conf` 目前包含：

- SPA 路由回退：`try_files $uri $uri/ /index.html`
- `/api/` 反代到 `backend:8000`
- `/static/` 反代到 `backend:8000`（上传图片）
- `client_max_body_size 6m`（允许 5MB 图片）
- 静态资源 30 天缓存
- 使用 `location ^~ /static/`，避免被图片缓存正则拦截

生产环境还需要：

```nginx
listen 443 ssl;
ssl_certificate     /etc/nginx/certs/fullchain.pem;
ssl_certificate_key /etc/nginx/certs/privkey.pem;
```

并在 80 端口增加跳转到 HTTPS 的 server 块，或者使用 Caddy 自动管理证书。

---

## 七、生产 VPS 部署

### 7.1 服务器规格

| 规格 | 建议 |
|---|---|
| CPU/内存 | 2C2G 起步，2C4G 更稳 |
| 磁盘 | 40GB+ SSD |
| 系统 | Ubuntu 22.04 / 24.04 LTS |
| Swap | 建议 2GB，防止构建 OOM |

### 7.2 安装 Docker

```bash
# 以 Ubuntu 官方仓库安装为例
sudo apt update
sudo apt install -y ca-certificates curl gnupg
# 按 Docker 官方文档添加 GPG key 和 apt 源
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl enable --now docker
```

> 使用 `docker compose`（v2 插件），不要依赖已停止维护的 `docker-compose` v1。

### 7.3 基础安全

```bash
# 创建部署用户（示例）
sudo adduser deploy
sudo usermod -aG docker deploy

# 防火墙只开放 SSH / HTTP / HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

SSH 建议：

- 使用密钥登录
- 禁用 root 密码登录
- 安装 fail2ban

### 7.4 域名与备案

- 大陆服务器 + 域名：需要 ICP 备案
- 香港/海外服务器：不需要备案，但国内访问速度可能较慢
- DNS 将域名 A 记录指向 VPS 公网 IP

### 7.5 部署代码

```bash
sudo mkdir -p /opt/personal-center
sudo chown $USER:$USER /opt/personal-center
git clone <your-repo> /opt/personal-center
cd /opt/personal-center
```

### 7.6 配置环境变量

```bash
# Compose 变量
cp docker-compose.env.example .env
# 编辑 .env：
#   FRONTEND_PORT=80
#   PUBLIC_ORIGIN=https://your-domain.com
#   MYSQL_* 使用强随机密码

# 后端变量
cp backend/.env.production.example backend/.env.production
# 编辑：
#   SECRET_KEY 强随机
#   ADMIN_PASSWORD 强密码
#   CORS_ORIGINS=https://your-domain.com

chmod 600 .env backend/.env.production
```

### 7.7 构建、迁移、启动

```bash
docker compose build
docker compose run --rm backend python init_db.py
docker compose up -d
docker compose ps
```

### 7.8 HTTPS

**方案 A：Caddy（推荐，自动续期）**

在 VPS 上安装 Caddy，反向代理到 `127.0.0.1:8080`，由 Caddy 自动申请 Let's Encrypt 证书。

**方案 B：Nginx + Certbot**

- 在 frontend 容器挂载 `./certs`
- 使用 Certbot webroot 或 DNS challenge 申请证书
- 配置自动续期

**方案 C：Cloudflare 代理**

- DNS 走 Cloudflare（橙色云）
- 源站使用 Cloudflare Origin Certificate
- SSL 模式设为 Full (Strict)

---

## 八、数据库迁移与初始化

`init_db.py` 会：

1. 执行 `alembic upgrade head`
2. 检测旧库（已有三张表但没有 `alembic_version`）并自动 `stamp head`
3. 创建管理员账号
4. 创建默认个人信息（如果不存在）

常用命令：

```bash
# 初始化
docker compose run --rm backend python init_db.py

# 只执行迁移
docker compose run --rm backend alembic upgrade head

# 新建迁移（修改模型后）
docker compose run --rm backend alembic revision --autogenerate -m "描述"

# 查看历史
docker compose run --rm backend alembic history
```

> 生产环境执行迁移前先备份数据库。

---

## 九、更新与回滚

### 9.1 更新

```bash
git pull
docker compose build backend frontend
docker compose run --rm backend python init_db.py
docker compose up -d
docker image prune -f
```

单机更新通常有几秒到几十秒的短暂停机，个人站可以接受。

### 9.2 回滚

```bash
git checkout <上一个稳定 commit 或 tag>
docker compose build backend frontend
docker compose up -d
```

注意：

- 如果数据库迁移已经执行，代码回滚不一定能回滚表结构；
- 重要更新前先备份数据库；
- 需要严格回滚时，按 Alembic 的 downgrade 或从备份恢复。

---

## 十、备份与恢复

### 10.1 备份 MySQL

```bash
mkdir -p backups
docker compose exec -T mysql sh -c \
  'exec mysqldump -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" \
   --single-transaction --routines --triggers "$MYSQL_DATABASE"' \
  > backups/db-$(date +%F).sql
```

### 10.2 备份上传图片

```bash
docker run --rm \
  -v personal-center_uploads_data:/data \
  -v "$PWD/backups":/backup \
  alpine tar czf /backup/uploads-$(date +%F).tar.gz -C /data .
```

### 10.3 恢复

```bash
# 数据库
cat backups/db-YYYY-MM-DD.sql | \
  docker compose exec -T mysql sh -c \
  'exec mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE"'

# 上传图片
docker run --rm \
  -v personal-center_uploads_data:/data \
  -v "$PWD/backups":/backup \
  alpine sh -c "cd /data && tar xzf /backup/uploads-YYYY-MM-DD.tar.gz"
```

建议：

- 每天或每周备份
- 至少保留 7~30 天
- 备份同步到对象存储或另一台机器
- 定期做恢复演练

---

## 十一、安全清单

- [ ] 修改默认管理员密码（后台路径：`/admin/password`，需输入当前密码）
- [ ] `SECRET_KEY` 使用强随机值
- [ ] MySQL 端口不映射到公网
- [ ] 后端 8000 端口不映射到公网
- [ ] UFW 只开放 22/80/443
- [ ] SSH 使用密钥登录，禁用 root 密码登录
- [ ] 配置 HTTPS，并开启 HTTP → HTTPS 跳转
- [ ] Nginx 设置 `client_max_body_size`
- [ ] 对 `/api/auth/login` 做限流
- [ ] Docker 日志轮转
- [ ] 定期更新系统和基础镜像
- [ ] 生产环境考虑关闭或限制 `/docs`
- [ ] 备份文件异地保存

---

## 十二、性能与资源

| 项目 | 建议 |
|---|---|
| VPS | 2C2G 起步，2C4G 更稳 |
| Swap | 2GB，防止前端构建 OOM |
| Uvicorn workers | 2 左右 |
| MySQL buffer pool | 按内存调整，256~512MB 起步 |
| 静态资源 | Nginx gzip + 30 天缓存 |
| 图片 | 量大后迁移到 OSS/COS/R2 + CDN |
| 构建 | 内存不足时在本地/CI 构建镜像，VPS 只拉取 |

---

## 十三、常见问题排查

| 现象 | 可能原因 | 处理 |
|---|---|---|
| 页面 502 | backend 未启动 / 不健康 | `docker compose ps`、看 backend 日志、检查数据库连接 |
| MySQL unhealthy | 密码错误 / volume 初始化失败 | 检查 `.env`、`docker compose logs mysql` |
| 上传返回 413 | Nginx 默认 1MB | 确认 `client_max_body_size 6m` |
| 图片 404 | `/static/` 未反代或被正则拦截 | 检查 `location ^~ /static/` |
| `npm ci` 失败 | `package-lock.json` 被 .dockerignore 排除 | 保留锁文件 |
| `vite: not found` | 构建阶段只装了生产依赖 | 使用 `npm ci`，不要 `--only=production` |
| npm `ECONNRESET` | 容器访问 npm 官方源不稳定 | 在 `.env` 设置 `NPM_REGISTRY=https://registry.npmmirror.com` 后重建 frontend |
| 首次启动 unhealthy | 用 `/api/profile` 做健康检查 | 改用 `/health` |
| 构建 OOM | 2G 内存构建前端 | 加 swap 或改在 CI 构建 |
| 端口冲突 | 80/8080 被占用 | 修改 `FRONTEND_PORT` |
| CORS 报错 | `PUBLIC_ORIGIN` 不对 | 改为实际访问地址并重启 backend |

常用排查命令：

```bash
docker compose ps
docker compose logs -f --tail=200 backend
docker compose logs -f --tail=200 mysql
docker compose exec backend curl -f http://localhost:8000/health
docker compose exec backend python -c "import os; print(os.getenv('DATABASE_URL'))"
```

---

## 十四、当前项目已完成的部署适配

| 文件 | 修改 |
|---|---|
| `frontend/Dockerfile` | Node 22；`npm ci` 安装全部依赖；支持 `NPM_REGISTRY`；健康检查改为 `127.0.0.1` |
| `frontend/.dockerignore` | 不再排除 `package-lock.json` |
| `frontend/nginx.conf` | 新增 `/static/` 反代、修正上传路径、6MB 上传限制、`^~` 防止正则抢占 |
| `backend/Dockerfile` | Python 3.11；非 root 用户；健康检查改为 `/health`；精简系统依赖 |
| `backend/.dockerignore` | 排除所有 `.env*`，防止密钥进入镜像 |
| `docker-compose.yml` | 新增 MySQL/backend/frontend、volume、健康检查、日志轮转、`NPM_REGISTRY` 构建参数 |
| `docker-compose.env.example` | Compose 变量示例 |
| `backend/.env.production.example` | 后端配置示例 |
| `.gitignore` | 忽略 `.env.production`、`backups/`、`certs/`、`data/` |

---

## 十五、上线检查清单

- [ ] DNS 已指向服务器
- [ ] 服务器防火墙只开放 22/80/443
- [ ] `.env` 和 `backend/.env.production` 已改为强密码
- [ ] `FRONTEND_PORT=80`
- [ ] `PUBLIC_ORIGIN=https://你的域名`
- [ ] `docker compose config --quiet` 通过
- [ ] `docker compose build` 成功
- [ ] `python init_db.py` 成功
- [ ] `docker compose ps` 三个服务健康
- [ ] 首页、项目详情、管理后台可访问
- [ ] 图片上传和访问正常
- [ ] HTTPS 证书有效
- [ ] 数据库和上传目录备份任务已配置
- [ ] 已测试一次恢复流程

---

## 十六、本次本地部署记录（2026-11-01）

### 环境

- Windows 11 + Docker Desktop 29.6.1
- Docker Compose v5.2.0
- Docker Linux VM 内存：约 4GB

### 部署结果

| 服务 | 镜像 | 状态 | 端口 |
|---|---|---|---|
| frontend | `personal-center-frontend` | healthy | `0.0.0.0:8080 -> 80` |
| backend | `personal-center-backend` | healthy | 仅内网 8000 |
| mysql | `mysql:8.0` | healthy | 仅内网 3306 |

访问地址：

- 首页：http://localhost:8080
- 管理后台：http://localhost:8080/admin/login
- 管理员：`admin`
- 密码：`backend/.env.production` 中的 `ADMIN_PASSWORD`

### 验证结果

| 项目 | 结果 |
|---|---|
| 首页 HTML | 200 |
| `/api/profile` | 200 |
| `/api/projects` | 200 |
| 管理员登录 | 200 |
| 图片上传 | 200 |
| `/static/uploads/...` 访问 | 200，`image/png` |
| 上传测试文件清理 | 成功 |

### 本次环境备注

- Docker Desktop 原有的 USTC / 163 镜像加速器返回 EOF，本次使用显式 `registry-1.docker.io/library/...` 拉取后打本地 tag，未修改全局 daemon 配置。
- 前端容器内访问 npm 官方源出现 `ECONNRESET`，本地 `.env` 设置了：

  ```ini
  NPM_REGISTRY=https://registry.npmmirror.com
  ```

- 前端健康检查由 `http://localhost/` 改为 `http://127.0.0.1/`，避免容器内 IPv6 解析导致 unhealthy。
- Compose 初次启动时是默认个人信息（`YOUR NAME`）和 0 个项目；随后已完成本地数据迁移，详见下一节。

### 本地数据迁移记录（2026-11-01）

迁移内容：

- 本地 `profile`（`aass`）→ Compose
- 本地 `project` 6 条 → Compose
- 本地上传文件 39 个 → `uploads_data` volume
- 管理员账号保留 Compose 生成的强密码，**未导入本地开发管理员密码**

迁移前备份（位于 `backups/`，已被 Git 忽略）：

- `compose-before-migration-20261101-103553.sql`：Compose 迁移前的种子数据
- `local-content-20261101-103553.sql`：本地 `profile` / `project` 数据

处理方式：

1. 只导出本地 `profile`、`project`，不导出 `admin_user`
2. 清空 Compose 的 `profile`、`project` 后导入
3. 复制 `backend/uploads` 到容器 `/app/uploads` 并修正属主

迁移后验证：

| 项目 | 结果 |
|---|---|
| profile | 1 条，`aass` |
| project | 6 条 |
| admin_user | 1 条，Compose 密码仍可登录 |
| uploads | 39 个文件 |
| 项目图片 | `/static/uploads/...` 返回 200 |

> 本地开发库没有被修改。备份文件是完整 SQL 转储，回滚前需要先评估目标表状态，避免与现有表冲突。

---

## 附录：常用命令速查

```bash
docker compose config --quiet       # 校验配置
docker compose build                # 构建镜像
docker compose up -d                # 启动
docker compose ps                   # 状态
docker compose logs -f backend      # 日志
docker compose restart backend      # 重启
docker compose run --rm backend python init_db.py
docker compose exec backend sh      # 进入容器
docker compose down                 # 停止，保留数据
docker compose down -v              # 停止并删除数据卷（危险）
```
