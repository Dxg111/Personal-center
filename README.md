# Personal Center - 个人中心站点

> 基于 Vue3 + FastAPI 的全栈个人中心项目
> 
> 版本：v1.0.0 MVP

## 🎉 项目完成情况

### ✅ 已完成功能（MVP 全部完成）

**后端 API（100%）：**
- ✅ FastAPI + SQLModel + MySQL 架构
- ✅ JWT 认证系统
- ✅ 用户管理（管理员登录）
- ✅ 项目 CRUD（创建、读取、更新、删除）
- ✅ 草稿/发布状态管理
- ✅ 个人信息管理
- ✅ 图片上传功能
- ✅ 浏览量统计
- ✅ 分类筛选（项目/作品）
- ✅ 完整单元测试（17/17 通过）

**前端页面（100%）：**

访客端：
- ✅ 首页（科幻工科风格 Hero + 雷达动画 + 打字机效果）
- ✅ 项目列表展示（支持分类切换）
- ✅ 项目详情页（Markdown 渲染 + 浏览量统计）
- ✅ 404 页面（雷达失败动画）
- ✅ 终端风格页脚

管理端：
- ✅ 登录页面（JWT 认证）
- ✅ 项目列表（统计数据 + 状态管理）
- ✅ 项目编辑（支持 Markdown + 图片上传）
- ✅ 草稿/发布功能
- ✅ 个人信息编辑
- ✅ 路由守卫（权限控制）

**视觉效果（100%）：**
- ✅ 鼠标光斑跟随
- ✅ 网格线背景
- ✅ 雷达扫描动画
- ✅ 打字机 slogan 效果
- ✅ 状态指示灯闪烁
- ✅ 卡片 hover 动效
- ✅ 切角设计元素
- ✅ 科幻深色主题（访客端绿色 #00ffc8 + 管理端黄色 #ffb020）

---

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- MySQL 8.0+

### 1. 后端启动

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置数据库
# 编辑 .env 文件，设置数据库连接信息

# 创建数据库
mysql -u root -p
CREATE DATABASE personal_center CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 初始化数据库
python init_db.py

# 启动服务
uvicorn app.main:app --reload --port 8000
```

后端服务：http://localhost:8000
API 文档：http://localhost:8000/docs

**默认管理员账号：**
- 用户名：`admin`
- 密码：`123456`

### 2. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务：http://localhost:5173

---

## 📁 项目结构

```
Personal-center/
├── backend/                    # 后端
│   ├── app/
│   │   ├── main.py            # FastAPI 入口
│   │   ├── config.py          # 配置管理
│   │   ├── database.py        # 数据库连接
│   │   ├── models/            # 数据模型
│   │   │   ├── user.py        # 管理员用户
│   │   │   ├── project.py     # 项目
│   │   │   └── profile.py     # 个人信息
│   │   ├── schemas/           # 请求/响应模型
│   │   ├── api/               # API 路由
│   │   │   ├── auth.py        # 认证
│   │   │   ├── projects.py    # 项目（公开）
│   │   │   ├── profile.py     # 个人信息（公开）
│   │   │   └── admin.py       # 管理端
│   │   └── utils/             # 工具函数
│   │       ├── auth.py        # JWT 认证
│   │       └── upload.py      # 文件上传
│   ├── uploads/               # 上传文件
│   ├── init_db.py            # 数据库初始化
│   ├── test_main.py          # 单元测试
│   ├── test_api.py           # API 集成测试
│   ├── requirements.txt      # 依赖列表
│   └── .env                  # 环境变量
│
├── frontend/                  # 前端
│   ├── src/
│   │   ├── views/
│   │   │   ├── public/       # 访客端页面
│   │   │   │   ├── Home.vue           # 首页
│   │   │   │   ├── ProjectDetail.vue  # 项目详情
│   │   │   │   └── NotFound.vue       # 404
│   │   │   └── admin/        # 管理端页面
│   │   │       ├── Login.vue          # 登录
│   │   │       ├── ProjectList.vue    # 项目列表
│   │   │       ├── ProjectEdit.vue    # 项目编辑
│   │   │       └── ProfileEdit.vue    # 个人信息编辑
│   │   ├── router/           # 路由配置
│   │   ├── stores/           # Pinia 状态管理
│   │   ├── api/              # API 封装
│   │   ├── assets/           # 静态资源
│   │   ├── style.css         # 全局样式
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
│
└── docx/                      # 文档
    ├── 需求分析文档.md
    └── 方案设计文档.md
```

---

## 🔌 API 接口

### 公开接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/profile` | 获取个人信息 |
| GET | `/api/projects` | 获取项目列表（支持 category 和 published 过滤） |
| GET | `/api/projects/featured` | 获取首页重点项目 |
| GET | `/api/projects/{id}` | 获取项目详情（浏览量 +1） |

### 认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/login` | 管理员登录 |

### 管理接口（需要 JWT Token）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/admin/projects` | 获取后台项目列表（含草稿） |
| POST | `/api/admin/projects` | 创建项目 |
| PUT | `/api/admin/projects/{id}` | 编辑项目 |
| DELETE | `/api/admin/projects/{id}` | 删除项目 |
| PUT | `/api/admin/projects/{id}/publish` | 切换发布/草稿状态 |
| GET | `/api/admin/profile` | 获取个人信息 |
| PUT | `/api/admin/profile` | 更新个人信息 |
| POST | `/api/admin/upload` | 上传图片 |

---

## 🎨 设计风格

### 访客端（公开站点）
- **主色调**：荧光绿 `#00ffc8`
- **背景**：深蓝黑 `#050810`
- **风格**：科幻工科风，雷达扫描、网格线、终端元素

### 管理端（后台）
- **主色调**：黄色 `#ffb020`（区分访客端）
- **背景**：深蓝黑 `#050810`
- **风格**：控制台风格，表格数据展示

### 字体
- 正文：系统默认字体
- 代码/终端：JetBrains Mono
- 标题：Rajdhani

---

## 🧪 测试

### 后端测试

```bash
cd backend

# 运行单元测试
pytest test_main.py -v

# 运行 API 集成测试
python test_api.py
```

所有测试通过：
- ✅ 15/15 API 接口测试通过
- ✅ 17/17 单元测试通过

---

## 📝 使用说明

### 1. 首次使用

1. 启动后端和前端服务
2. 访问 http://localhost:5173
3. 点击右上角进入管理后台（或直接访问 http://localhost:5173/admin/login）
4. 使用默认账号登录：`admin` / `123456`
5. 编辑个人信息
6. 创建第一个项目

### 2. 创建项目

1. 登录后台 → 点击"+ 新建"
2. 填写项目信息：
   - 标题、简介
   - 分类（项目/作品）
   - 技术栈（逗号分隔）
   - 上传封面图
   - 演示链接、GitHub 链接
   - 正文（支持 Markdown）
3. 选择"存草稿"或"发布"

### 3. 管理项目

- **编辑**：修改项目内容
- **发布/取消发布**：切换项目状态
- **删除**：永久删除项目
- **排序**：通过 sort_order 控制首页展示顺序

---

## 🔐 安全性

- ✅ JWT Token 认证
- ✅ 密码 bcrypt 哈希
- ✅ SQL 注入防护（ORM 参数化）
- ✅ XSS 防护（DOMPurify 清洗 HTML）
- ✅ 文件上传验证（类型、大小限制）
- ✅ 路由守卫（未登录自动跳转）

---

## 🚧 后续扩展（P1-P3）

### P1 - 第二优先级
- [ ] 文章/博客模块
- [ ] 项目扩展标签（角色、周期、类型）

### P2 - 第三优先级
- [ ] AI 智能问答（右下角气泡）
- [ ] 深色/浅色模式切换
- [ ] GitHub 贡献图嵌入
- [ ] 文章目录自动生成

### P3 - 第四优先级
- [ ] 后台数据看板（浏览趋势、访客来源）
- [ ] 时间线经历页

---

## 📄 License

MIT

---

## 👤 作者

DXG

---

**🎉 MVP 已完成，所有核心功能可用！**

访问地址：
- 前端：http://localhost:5173
- 后端 API：http://localhost:8000/docs
- 管理后台：http://localhost:5173/admin/login
