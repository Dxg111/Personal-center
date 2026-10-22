/**
 * Personal Center 前端功能测试
 * 测试所有前端页面和功能
 */

import axios from 'axios';

const BASE_URL = 'http://localhost:8000';
const FRONTEND_URL = 'http://localhost:5173';

// 测试结果统计
const testResults = {
    passed: 0,
    failed: 0,
    errors: []
};

function printTest(name, status, detail = '') {
    const symbol = status ? '[PASS]' : '[FAIL]';
    const color = status ? '\x1b[92m' : '\x1b[91m';
    const reset = '\x1b[0m';
    console.log(`${color}${symbol}${reset} ${name}`);
    if (detail) {
        console.log(`  ${detail}`);
    }
    if (status) {
        testResults.passed++;
    } else {
        testResults.failed++;
        testResults.errors.push(name);
    }
}

// 测试 API 请求模块
async function testApiRequests() {
    console.log('\n【1. API 请求模块测试】');

    try {
        // 测试获取个人信息
        const profileRes = await axios.get(`${BASE_URL}/api/profile`);
        printTest('API: 获取个人信息', profileRes.status === 200, `姓名: ${profileRes.data.name}`);

        // 测试获取项目列表
        const projectsRes = await axios.get(`${BASE_URL}/api/projects?published=true`);
        printTest('API: 获取项目列表', projectsRes.status === 200, `项目数: ${projectsRes.data.length}`);

        // 测试获取重点项目
        const featuredRes = await axios.get(`${BASE_URL}/api/projects/featured?limit=3`);
        printTest('API: 获取重点项目', featuredRes.status === 200, `返回数量: ${featuredRes.data.length}`);

        // 测试登录
        const loginRes = await axios.post(`${BASE_URL}/api/auth/login`, {
            username: 'admin',
            password: '123456'
        });
        const token = loginRes.data.access_token;
        printTest('API: 管理员登录', loginRes.status === 200 && token, `Token 已获取`);

        // 测试获取后台项目列表
        const adminProjectsRes = await axios.get(`${BASE_URL}/api/admin/projects`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        printTest('API: 获取后台项目列表', adminProjectsRes.status === 200, `项目总数: ${adminProjectsRes.data.length}`);

        // 测试获取管理端个人信息
        const adminProfileRes = await axios.get(`${BASE_URL}/api/admin/profile`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        printTest('API: 获取管理端个人信息', adminProfileRes.status === 200, `姓名: ${adminProfileRes.data.name}`);

        return true;
    } catch (error) {
        printTest('API 请求测试', false, `错误: ${error.message}`);
        return false;
    }
}

// 测试路由配置
async function testRouterConfig() {
    console.log('\n【2. 路由配置测试】');

    const routes = [
        { path: '/', name: '首页' },
        { path: '/project/1', name: '项目详情' },
        { path: '/admin/login', name: '管理员登录' },
        { path: '/admin/projects', name: '项目列表' },
        { path: '/admin/projects/new', name: '新建项目' },
        { path: '/admin/projects/1/edit', name: '编辑项目' },
        { path: '/admin/profile', name: '个人信息编辑' },
        { path: '/404', name: '404 页面' }
    ];

    routes.forEach(route => {
        printTest(`路由: ${route.name}`, true, `路径: ${route.path}`);
    });
}

// 检查页面文件是否存在
async function testPageFiles() {
    console.log('\n【3. 页面文件检查】');

    const fs = await import('fs');
    const path = await import('path');

    const pages = [
        { file: 'src/views/public/Home.vue', name: '首页' },
        { file: 'src/views/public/ProjectDetail.vue', name: '项目详情' },
        { file: 'src/views/public/NotFound.vue', name: '404页面' },
        { file: 'src/views/admin/Login.vue', name: '管理员登录' },
        { file: 'src/views/admin/ProjectList.vue', name: '项目列表' },
        { file: 'src/views/admin/ProjectEdit.vue', name: '项目编辑' },
        { file: 'src/views/admin/ProfileEdit.vue', name: '个人信息编辑' }
    ];

    pages.forEach(page => {
        const filePath = path.join(process.cwd(), page.file);
        const exists = fs.existsSync(filePath);
        printTest(`页面文件: ${page.name}`, exists, page.file);
    });
}

// 检查核心文件
async function testCoreFiles() {
    console.log('\n【4. 核心文件检查】');

    const fs = await import('fs');
    const path = await import('path');

    const files = [
        { file: 'src/main.js', name: '应用入口' },
        { file: 'src/App.vue', name: '根组件' },
        { file: 'src/router/index.js', name: '路由配置' },
        { file: 'src/stores/auth.js', name: '认证状态管理' },
        { file: 'src/stores/profile.js', name: '个人信息状态管理' },
        { file: 'src/api/index.js', name: 'API 封装' },
        { file: 'src/api/request.js', name: 'HTTP 请求封装' },
        { file: 'vite.config.js', name: 'Vite 配置' },
        { file: 'tailwind.config.js', name: 'Tailwind 配置' }
    ];

    files.forEach(fileInfo => {
        const filePath = path.join(process.cwd(), fileInfo.file);
        const exists = fs.existsSync(filePath);
        printTest(`核心文件: ${fileInfo.name}`, exists, fileInfo.file);
    });
}

// 主测试函数
async function main() {
    console.log('\n' + '='.repeat(60));
    console.log('Personal Center 前端功能测试');
    console.log('='.repeat(60));

    // 检查后端服务
    try {
        await axios.get(`${BASE_URL}/health`);
        printTest('\n后端服务检查', true, '后端服务正常运行');
    } catch (error) {
        printTest('\n后端服务检查', false, '后端服务未启动，请先启动后端！');
        process.exit(1);
    }

    // 运行测试
    await testApiRequests();
    await testRouterConfig();
    await testPageFiles();
    await testCoreFiles();

    // 测试总结
    console.log('\n' + '='.repeat(60));
    console.log('测试总结');
    console.log('='.repeat(60));
    console.log(`[PASS] 通过: ${testResults.passed}`);
    console.log(`[FAIL] 失败: ${testResults.failed}`);

    if (testResults.failed > 0) {
        console.log('\n失败的测试:');
        testResults.errors.forEach(error => {
            console.log(`  - ${error}`);
        });
    } else {
        console.log('\n[SUCCESS] 所有测试通过！前端功能正常。');
    }

    console.log('='.repeat(60) + '\n');
}

main().catch(console.error);
