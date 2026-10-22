# 测试命令快速参考

## 🧪 运行所有测试

### 后端测试

```bash
# 1. 单元测试
cd backend
pytest test_main.py -v

# 预期结果：17 passed

# 2. API 集成测试（需要先启动后端服务）
cd backend
python test_api.py

# 预期结果：[PASS] 通过: 15, [FAIL] 失败: 0
```

### 前端测试

```bash
# 1. 功能测试（需要后端服务运行）
cd frontend
node test_frontend.js

# 预期结果：[PASS] 通过: 31, [FAIL] 失败: 0

# 2. 构建测试
cd frontend
npm run build

# 预期结果：✓ built in 4.26s
```

---

## 🚀 启动服务

### 后端
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 前端
```bash
cd frontend
npm run dev
```

---

## 📊 测试结果总览

| 测试类型 | 命令 | 预期结果 |
|---------|------|----------|
| 后端单元测试 | `pytest test_main.py -v` | 17/17 通过 |
| 后端集成测试 | `python test_api.py` | 15/15 通过 |
| 前端功能测试 | `node test_frontend.js` | 31/31 通过 |
| 前端构建测试 | `npm run build` | 构建成功 |

**总计：63/63 测试通过 (100%)**

---

## 🔗 访问地址

- 前端：http://localhost:5173
- 管理后台：http://localhost:5173/admin/login
- API 文档：http://localhost:8000/docs
- 默认账号：admin / 123456
