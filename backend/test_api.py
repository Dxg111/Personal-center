import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

# 测试结果统计
test_results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}

def print_test(name, status, detail=""):
    """打印测试结果"""
    symbol = "[PASS]" if status else "[FAIL]"
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    try:
        print(f"{color}{symbol}{reset} {name}")
    except UnicodeEncodeError:
        print(f"{symbol} {name}")
    if detail:
        try:
            print(f"  {detail}")
        except UnicodeEncodeError:
            print(f"  {detail.encode('utf-8', errors='replace').decode('utf-8')}")
    if status:
        test_results["passed"] += 1
    else:
        test_results["failed"] += 1
        test_results["errors"].append(name)

def test_health_check():
    """测试健康检查"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        success = response.status_code == 200 and response.json()["status"] == "ok"
        print_test("健康检查", success, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("健康检查", False, f"错误: {str(e)}")
        return False

def test_login():
    """测试登录并返回 token"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": "admin", "password": "123456"}
        )
        success = response.status_code == 200 and "access_token" in response.json()
        if success:
            token = response.json()["access_token"]
            print_test("管理员登录", True, f"Token: {token[:20]}...")
            return token
        else:
            print_test("管理员登录", False, f"状态码: {response.status_code}")
            return None
    except Exception as e:
        print_test("管理员登录", False, f"错误: {str(e)}")
        return None

def test_login_wrong_password():
    """测试错误密码"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": "admin", "password": "wrongpass"}
        )
        success = response.status_code == 401
        print_test("登录错误密码验证", success, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("登录错误密码验证", False, f"错误: {str(e)}")
        return False

def test_get_profile():
    """测试获取个人信息（公开）"""
    try:
        response = requests.get(f"{BASE_URL}/api/profile")
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test("获取个人信息（公开）", True, f"姓名: {data.get('name', 'N/A')}")
        else:
            print_test("获取个人信息（公开）", False, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("获取个人信息（公开）", False, f"错误: {str(e)}")
        return False

def test_get_projects():
    """测试获取项目列表（公开）"""
    try:
        response = requests.get(f"{BASE_URL}/api/projects?published=true")
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test("获取项目列表（公开）", True, f"项目数: {len(data)}")
        else:
            print_test("获取项目列表（公开）", False, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("获取项目列表（公开）", False, f"错误: {str(e)}")
        return False

def test_get_featured_projects():
    """测试获取重点项目"""
    try:
        response = requests.get(f"{BASE_URL}/api/projects/featured?limit=3")
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test("获取重点项目", True, f"返回数量: {len(data)}")
        else:
            print_test("获取重点项目", False, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("获取重点项目", False, f"错误: {str(e)}")
        return False

def test_create_project(token):
    """测试创建项目"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        project_data = {
            "title": "测试项目 - API Test",
            "summary": "这是一个通过 API 测试创建的项目",
            "content": "# 测试项目\n\n这是正文内容",
            "tech_stack": "Python,FastAPI,Vue3",
            "category": "project",
            "is_published": True,
            "sort_order": 10
        }
        response = requests.post(
            f"{BASE_URL}/api/admin/projects",
            json=project_data,
            headers=headers
        )
        success = response.status_code == 200
        if success:
            data = response.json()
            project_id = data.get("id")
            print_test("创建项目", True, f"项目ID: {project_id}, 标题: {data.get('title')}")
            return project_id
        else:
            print_test("创建项目", False, f"状态码: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print_test("创建项目", False, f"错误: {str(e)}")
        return None

def test_get_admin_projects(token):
    """测试获取后台项目列表"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/admin/projects", headers=headers)
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test("获取后台项目列表", True, f"项目总数: {len(data)}")
        else:
            print_test("获取后台项目列表", False, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("获取后台项目列表", False, f"错误: {str(e)}")
        return False

def test_update_project(token, project_id):
    """测试更新项目"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        update_data = {
            "title": "测试项目 - 已更新",
            "summary": "更新后的简介",
            "content": "# 更新后的内容",
            "tech_stack": "Python,FastAPI,Vue3,MySQL",
            "category": "work",
            "sort_order": 5
        }
        response = requests.put(
            f"{BASE_URL}/api/admin/projects/{project_id}",
            json=update_data,
            headers=headers
        )
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test("更新项目", True, f"新标题: {data.get('title')}")
        else:
            print_test("更新项目", False, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("更新项目", False, f"错误: {str(e)}")
        return False

def test_toggle_publish(token, project_id):
    """测试切换发布状态"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(
            f"{BASE_URL}/api/admin/projects/{project_id}/publish",
            json={"is_published": False},
            headers=headers
        )
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test("切换发布状态", True, f"is_published: {data.get('is_published')}")
        else:
            print_test("切换发布状态", False, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("切换发布状态", False, f"错误: {str(e)}")
        return False

def test_get_project_detail(project_id):
    """测试获取项目详情（公开，浏览量+1）"""
    try:
        response = requests.get(f"{BASE_URL}/api/projects/{project_id}")
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test("获取项目详情", True, f"标题: {data.get('title')}, 浏览量: {data.get('views_count')}")
        else:
            print_test("获取项目详情", False, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("获取项目详情", False, f"错误: {str(e)}")
        return False

def test_get_admin_profile(token):
    """测试获取个人信息（管理端）"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/admin/profile", headers=headers)
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test("获取个人信息（管理端）", True, f"姓名: {data.get('name')}")
        else:
            print_test("获取个人信息（管理端）", False, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("获取个人信息（管理端）", False, f"错误: {str(e)}")
        return False

def test_update_profile(token):
    """测试更新个人信息"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        # 先获取当前信息
        response = requests.get(f"{BASE_URL}/api/admin/profile", headers=headers)
        if response.status_code != 200:
            print_test("更新个人信息（获取失败）", False, "无法获取当前个人信息")
            return False

        current = response.json()
        # 更新信息
        update_data = {
            "name": current.get("name") + " (测试)",
            "avatar_url": current.get("avatar_url"),
            "bio": "这是通过 API 测试更新的简介",
            "typing_slogan": "> API 测试中...",
            "wechat": current.get("wechat"),
            "email": current.get("email"),
            "github_url": current.get("github_url")
        }
        response = requests.put(
            f"{BASE_URL}/api/admin/profile",
            json=update_data,
            headers=headers
        )
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test("更新个人信息", True, f"新姓名: {data.get('name')}")

            # 恢复原始数据
            restore_data = {
                "name": current.get("name"),
                "avatar_url": current.get("avatar_url"),
                "bio": current.get("bio"),
                "typing_slogan": current.get("typing_slogan"),
                "wechat": current.get("wechat"),
                "email": current.get("email"),
                "github_url": current.get("github_url")
            }
            requests.put(f"{BASE_URL}/api/admin/profile", json=restore_data, headers=headers)
        else:
            print_test("更新个人信息", False, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("更新个人信息", False, f"错误: {str(e)}")
        return False

def test_delete_project(token, project_id):
    """测试删除项目"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(
            f"{BASE_URL}/api/admin/projects/{project_id}",
            headers=headers
        )
        success = response.status_code == 200
        print_test("删除项目", success, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("删除项目", False, f"错误: {str(e)}")
        return False

def test_unauthorized_access():
    """测试未授权访问"""
    try:
        response = requests.get(f"{BASE_URL}/api/admin/projects")
        success = response.status_code == 403
        print_test("未授权访问拦截", success, f"状态码: {response.status_code}")
        return success
    except Exception as e:
        print_test("未授权访问拦截", False, f"错误: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("Personal Center 后端 API 完整测试")
    print("="*60 + "\n")

    # 1. 基础测试
    print("【1. 基础功能测试】")
    if not test_health_check():
        print("\n⚠️  后端服务未启动，请先启动后端服务！")
        return

    # 2. 认证测试
    print("\n【2. 认证功能测试】")
    test_login_wrong_password()
    token = test_login()
    if not token:
        print("\n⚠️  登录失败，无法继续测试需要认证的接口")
        return

    test_unauthorized_access()

    # 3. 公开接口测试
    print("\n【3. 公开接口测试】")
    test_get_profile()
    test_get_projects()
    test_get_featured_projects()

    # 4. 项目管理测试
    print("\n【4. 项目管理测试】")
    test_get_admin_projects(token)
    project_id = test_create_project(token)

    if project_id:
        test_update_project(token, project_id)
        test_toggle_publish(token, project_id)
        test_get_project_detail(project_id)
        test_delete_project(token, project_id)

    # 5. 个人信息管理测试
    print("\n【5. 个人信息管理测试】")
    test_get_admin_profile(token)
    test_update_profile(token)

    # 6. 测试总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"[PASS] 通过: {test_results['passed']}")
    print(f"[FAIL] 失败: {test_results['failed']}")

    if test_results['failed'] > 0:
        print("\n失败的测试:")
        for error in test_results['errors']:
            print(f"  - {error}")
    else:
        print("\n[SUCCESS] 所有测试通过！后端 API 功能正常。")

    print("="*60 + "\n")

if __name__ == "__main__":
    main()
