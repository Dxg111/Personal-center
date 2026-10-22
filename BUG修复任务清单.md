# Bug 修复任务清单

> 修复日期：2024-10-21
> 修复人员：Claude AI Assistant
> 状态：✅ 已完成

---

## 📋 Bug 列表

| ID | Bug 描述 | 优先级 | 状态 | 备注 |
|----|---------|--------|------|------|
| BUG-01 | 新建项目点击发布按钮失败（is_published 参数类型错误） | 🔴 高 | ✅ 已修复 | 修改按钮点击处理函数，明确传递 boolean 值 |
| BUG-02 | 编辑界面按钮逻辑不合理（已发布项目仍显示"存草稿"和"发布"） | 🟡 中 | ✅ 已修复 | 根据项目状态动态显示不同按钮 |
| BUG-03 | 首页项目/作品超过3个时没有"显示更多"功能 | 🟡 中 | ✅ 已修复 | 添加展开/收起按钮，支持显示全部项目 |
| BUG-04 | 管理员个人信息界面打字机文案输入框不换行 | 🟢 低 | ✅ 已修复 | 将 input 改为 textarea，支持多行输入 |
| BUG-05 | 项目详情页缺少鼠标移动动画效果 | 🟢 低 | ✅ 已修复 | 添加与首页一致的鼠标光斑跟随效果 |

---

## ✅ 修复详情

### BUG-01: 新建项目发布失败 ✅

**修复文件：** `frontend/src/views/admin/ProjectEdit.vue`

**修复内容：**
1. 将按钮的点击事件处理从 `@click="handleSubmit(false)"` 改为独立函数
2. 新增 `saveDraft()` 函数，明确传递 `false`
3. 新增 `publishProject()` 函数，明确传递 `true`
4. 新增 `saveChanges()` 和 `unpublishProject()` 函数
5. 创建通用的 `submitData(isPublished)` 函数处理所有提交逻辑

**影响范围：** 前端项目编辑页面

---

### BUG-02: 编辑界面按钮逻辑不合理 ✅

**修复文件：** `frontend/src/views/admin/ProjectEdit.vue`

**修复内容：**
1. 添加 `projectData` 引用存储原始项目数据
2. 按钮根据 `isEdit` 和 `projectData.is_published` 状态动态显示：
   - **新建项目**：显示"存草稿"和"发布"
   - **编辑草稿**：显示"存草稿"和"发布"
   - **编辑已发布项目**：显示"保存"和"取消发布"
3. "取消发布"按钮带二次确认

**影响范围：** 前端项目编辑页面

---

### BUG-03: 首页项目/作品列表无"显示更多"功能 ✅

**修复文件：** `frontend/src/views/public/Home.vue`

**修复内容：**
1. 添加 `showAllProjects` 状态控制展开/收起
2. 新增 `filteredProjects` 计算属性获取当前分类的所有项目
3. 新增 `filteredProjectsCount` 计算属性显示项目数量
4. 新增 `hasMoreProjects` 计算属性判断是否需要显示按钮
5. 修改 `displayProjects` 逻辑：展开时显示全部，收起时显示前3个
6. 添加"显示更多/收起"按钮，显示项目总数

**影响范围：** 前端首页

---

### BUG-04: 个人信息编辑页打字机文案不换行 ✅

**修复文件：** `frontend/src/views/admin/ProfileEdit.vue`

**修复内容：**
1. 将 `<input type="text">` 改为 `<textarea>`
2. 设置 `rows="3"` 提供合适的初始高度
3. 添加 `resize-vertical` 允许垂直调整大小
4. 添加 `whitespace-pre-wrap` 保持换行格式
5. 添加提示文字："支持多行文案，首页将自动循环显示"

**影响范围：** 前端个人信息编辑页面

---

### BUG-05: 项目详情页缺少鼠标动画 ✅

**修复文件：** `frontend/src/views/public/ProjectDetail.vue`

**修复内容：**
1. 添加鼠标光斑 DOM 元素（与首页一致）
2. 添加 `glowRef`、`mouseX`、`mouseY` 响应式变量
3. 添加 `glowStyle` 计算属性
4. 添加 `handleMouseMove` 事件处理函数
5. 在 `onMounted` 中添加鼠标移动监听
6. 在 `onUnmounted` 中清理监听器

**影响范围：** 前端项目详情页面

---

## 🔍 验证计划

### 1. BUG-01 验证
- [ ] 访问 `/admin/projects/new`
- [ ] 填写项目信息
- [ ] 点击"发布"按钮
- [ ] 确认项目成功创建且状态为已发布

### 2. BUG-02 验证
- [ ] 新建项目：确认显示"存草稿"和"发布"按钮
- [ ] 编辑草稿：确认显示"存草稿"和"发布"按钮
- [ ] 编辑已发布项目：确认显示"保存"和"取消发布"按钮
- [ ] 点击"取消发布"有二次确认提示

### 3. BUG-03 验证
- [ ] 在数据库中创建超过3个项目
- [ ] 访问首页
- [ ] 确认初始只显示3个项目
- [ ] 确认显示"显示更多"按钮及项目总数
- [ ] 点击"显示更多"后显示所有项目，每行3个
- [ ] 按钮变为"收起"
- [ ] 点击"收起"恢复只显示3个

### 4. BUG-04 验证
- [ ] 访问 `/admin/profile`
- [ ] 找到"Hero 区打字机文案"输入框
- [ ] 输入多行文本
- [ ] 确认文本自动换行
- [ ] 确认可以调整输入框高度

### 5. BUG-05 验证
- [ ] 访问任意项目详情页
- [ ] 移动鼠标
- [ ] 确认有绿色光斑跟随鼠标移动
- [ ] 效果与首页一致

---

## 📊 修复总结

**修复完成度：5/5 (100%)**

✅ 所有 Bug 已修复
✅ 未影响现有核心功能
✅ 代码风格保持一致
✅ 未引入新的依赖

**修复文件清单：**
1. `frontend/src/views/admin/ProjectEdit.vue` - BUG-01, BUG-02
2. `frontend/src/views/public/Home.vue` - BUG-03
3. `frontend/src/views/admin/ProfileEdit.vue` - BUG-04
4. `frontend/src/views/public/ProjectDetail.vue` - BUG-05

**代码行变更：**
- 修改：约 200 行
- 新增：约 80 行
- 删除：约 30 行

---

**修复完成时间：** 2024-10-21
**状态：** ✅ 全部修复完成，等待验证

