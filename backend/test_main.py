import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.main import app
from app.database import get_session
from app.models import AdminUser, Profile, Project
from app.utils.auth import get_password_hash
from app.utils.upload import detect_image_extension


# 测试数据库（内存 SQLite）
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="admin_user")
def admin_user_fixture(session: Session):
    """创建测试管理员"""
    admin = AdminUser(
        username="testadmin",
        hashed_password=get_password_hash("testpass123")
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)
    return admin


@pytest.fixture(name="profile")
def profile_fixture(session: Session):
    """创建测试个人信息"""
    profile = Profile(
        name="Test User",
        avatar_url="/static/avatar.jpg",
        bio="Test bio",
        typing_slogan="> Test slogan",
        wechat="test_wechat",
        email="test@example.com",
        github_url="https://github.com/test"
    )
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@pytest.fixture(name="auth_token")
def auth_token_fixture(client: TestClient, admin_user: AdminUser):
    """获取认证 Token"""
    response = client.post(
        "/api/auth/login",
        json={"username": "testadmin", "password": "testpass123"}
    )
    return response.json()["access_token"]


# ============ 测试认证 ============

def test_login_success(client: TestClient, admin_user: AdminUser):
    """测试登录成功"""
    response = client.post(
        "/api/auth/login",
        json={"username": "testadmin", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, admin_user: AdminUser):
    """测试密码错误"""
    response = client.post(
        "/api/auth/login",
        json={"username": "testadmin", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_login_wrong_username(client: TestClient):
    """测试用户名错误"""
    response = client.post(
        "/api/auth/login",
        json={"username": "nonexistent", "password": "testpass123"}
    )
    assert response.status_code == 401


# ============ 测试个人信息（公开） ============

def test_get_profile(client: TestClient, profile: Profile):
    """测试获取个人信息"""
    response = client.get("/api/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["bio"] == "Test bio"


def test_get_profile_not_found(client: TestClient):
    """测试个人信息不存在"""
    response = client.get("/api/profile")
    assert response.status_code == 404


# ============ 测试项目（公开） ============

def test_get_projects_empty(client: TestClient):
    """测试获取空项目列表"""
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert response.json() == []


def test_get_projects_published_only(client: TestClient, session: Session):
    """测试只返回已发布项目"""
    # 创建已发布项目
    published = Project(
        title="Published Project",
        summary="Summary",
        content="Content",
        is_published=True,
        category="project"
    )
    # 创建草稿项目
    draft = Project(
        title="Draft Project",
        summary="Summary",
        content="Content",
        is_published=False,
        category="project"
    )
    session.add(published)
    session.add(draft)
    session.commit()

    response = client.get("/api/projects?published=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Published Project"


def test_get_projects_by_category(client: TestClient, session: Session):
    """测试按分类过滤"""
    project1 = Project(
        title="Project 1",
        summary="Summary",
        content="Content",
        is_published=True,
        category="project"
    )
    project2 = Project(
        title="Work 1",
        summary="Summary",
        content="Content",
        is_published=True,
        category="work"
    )
    session.add(project1)
    session.add(project2)
    session.commit()

    response = client.get("/api/projects?category=work")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "work"


def test_get_projects_does_not_expose_drafts(client: TestClient, session: Session):
    """公开列表接口不能通过 published 查询参数暴露草稿"""
    published = Project(
        title="Published Project",
        summary="Summary",
        content="Content",
        is_published=True,
        category="project"
    )
    draft = Project(
        title="Draft Project",
        summary="Summary",
        content="Content",
        is_published=False,
        category="project"
    )
    session.add(published)
    session.add(draft)
    session.commit()

    # 尝试用 published=false 让接口返回草稿
    response = client.get("/api/projects?published=false")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Published Project"


def test_get_featured_projects(client: TestClient, session: Session):
    """测试获取重点项目"""
    for i in range(5):
        project = Project(
            title=f"Project {i}",
            summary="Summary",
            content="Content",
            is_published=True,
            sort_order=i,
            category="project"
        )
        session.add(project)
    session.commit()

    response = client.get("/api/projects/featured?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    # 验证按 sort_order 排序
    assert data[0]["title"] == "Project 0"


def test_get_project_detail(client: TestClient, session: Session):
    """测试获取项目详情"""
    project = Project(
        title="Test Project",
        summary="Summary",
        content="# Content",
        is_published=True,
        views_count=10,
        category="project"
    )
    session.add(project)
    session.commit()
    session.refresh(project)

    response = client.get(f"/api/projects/{project.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Project"
    assert data["views_count"] == 11  # 浏览量 +1


def test_get_project_not_found(client: TestClient):
    """测试项目不存在"""
    response = client.get("/api/projects/999")
    assert response.status_code == 404


def test_get_draft_detail_not_found(client: TestClient, session: Session):
    """访客不能通过 ID 直接访问草稿详情"""
    draft = Project(
        title="Draft Project",
        summary="Summary",
        content="Secret draft content",
        is_published=False,
        category="project"
    )
    session.add(draft)
    session.commit()
    session.refresh(draft)

    response = client.get(f"/api/projects/{draft.id}")
    assert response.status_code == 404


# ============ 测试项目管理（需认证） ============

def test_admin_get_draft_detail(client: TestClient, session: Session, auth_token: str):
    """管理端仍可查看草稿详情"""
    draft = Project(
        title="Draft Project",
        summary="Summary",
        content="Draft content",
        is_published=False,
        category="project"
    )
    session.add(draft)
    session.commit()
    session.refresh(draft)

    response = client.get(
        f"/api/admin/projects/{draft.id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Draft Project"


def test_create_project(client: TestClient, auth_token: str):
    """测试创建项目"""
    response = client.post(
        "/api/admin/projects",
        json={
            "title": "New Project",
            "summary": "Test summary",
            "content": "# Test content",
            "category": "project",
            "tech_stack": "Python,Vue3",
            "is_published": False,
            "sort_order": 1
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Project"
    assert data["is_published"] == False


def test_create_project_unauthorized(client: TestClient):
    """测试未认证创建项目"""
    response = client.post(
        "/api/admin/projects",
        json={
            "title": "New Project",
            "summary": "Summary",
            "content": "Content",
            "category": "project"
        }
    )
    assert response.status_code == 403


def test_update_project(client: TestClient, session: Session, auth_token: str):
    """测试更新项目"""
    project = Project(
        title="Old Title",
        summary="Old Summary",
        content="Old Content",
        category="project"
    )
    session.add(project)
    session.commit()
    session.refresh(project)

    response = client.put(
        f"/api/admin/projects/{project.id}",
        json={
            "title": "New Title",
            "summary": "New Summary",
            "content": "New Content",
            "category": "work",
            "tech_stack": "",
            "sort_order": 999
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["category"] == "work"


def test_delete_project(client: TestClient, session: Session, auth_token: str):
    """测试删除项目"""
    project = Project(
        title="To Delete",
        summary="Summary",
        content="Content",
        category="project"
    )
    session.add(project)
    session.commit()
    session.refresh(project)

    response = client.delete(
        f"/api/admin/projects/{project.id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200

    # 验证已删除
    deleted = session.get(Project, project.id)
    assert deleted is None


def test_toggle_publish(client: TestClient, session: Session, auth_token: str):
    """测试切换发布状态"""
    project = Project(
        title="Test",
        summary="Summary",
        content="Content",
        is_published=False,
        category="project"
    )
    session.add(project)
    session.commit()
    session.refresh(project)

    response = client.put(
        f"/api/admin/projects/{project.id}/publish",
        json={"is_published": True},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_published"] == True


def test_create_draft_with_minimal_fields(client: TestClient, auth_token: str):
    """草稿允许不填写任何内容"""
    response = client.post(
        "/api/admin/projects",
        json={},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == ""
    assert data["summary"] == ""
    assert data["content"] == ""
    assert data["is_published"] == False


def test_create_published_project_requires_title(client: TestClient, auth_token: str):
    """发布项目必须填写标题"""
    response = client.post(
        "/api/admin/projects",
        json={"is_published": True},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "发布项目前请填写标题"


def test_create_published_project_allows_empty_summary_and_content(
    client: TestClient, auth_token: str
):
    """发布项目只要求标题，简介和正文可以为空"""
    response = client.post(
        "/api/admin/projects",
        json={"title": "只有标题", "is_published": True},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "只有标题"
    assert data["summary"] == ""
    assert data["content"] == ""
    assert data["is_published"] == True


def test_update_published_project_cannot_clear_title(
    client: TestClient, session: Session, auth_token: str
):
    """已发布项目不能把标题改成空白"""
    project = Project(
        title="已发布项目",
        summary="",
        content="",
        is_published=True,
        category="project"
    )
    session.add(project)
    session.commit()
    session.refresh(project)

    response = client.put(
        f"/api/admin/projects/{project.id}",
        json={"title": "   "},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "发布项目前请填写标题"


def test_toggle_publish_requires_title(
    client: TestClient, session: Session, auth_token: str
):
    """没有标题的草稿不能发布"""
    draft = Project(
        title="",
        summary="",
        content="",
        is_published=False,
        category="project"
    )
    session.add(draft)
    session.commit()
    session.refresh(draft)

    response = client.put(
        f"/api/admin/projects/{draft.id}/publish",
        json={"is_published": True},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "发布项目前请填写标题"


def test_update_profile(client: TestClient, profile: Profile, auth_token: str):
    """测试更新个人信息"""
    response = client.put(
        "/api/admin/profile",
        json={
            "name": "Updated Name",
            "avatar_url": "/new-avatar.jpg",
            "bio": "Updated bio",
            "typing_slogan": "> Updated slogan",
            "wechat": "new_wechat",
            "email": "new@example.com",
            "github_url": "https://github.com/new"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["wechat"] == "new_wechat"


# ============ 测试图片上传 ============

def test_detect_image_extension():
    """根据文件头识别真实图片类型"""
    assert detect_image_extension(b"\xff\xd8\xff\xe0" + b"0" * 8) == ".jpg"
    assert detect_image_extension(b"\x89PNG\r\n\x1a\n" + b"0" * 8) == ".png"
    assert detect_image_extension(b"RIFF1234WEBP" + b"0" * 8) == ".webp"
    assert detect_image_extension(b"not an image") is None


def test_upload_rejects_spoofed_image(client: TestClient, auth_token: str):
    """伪装成图片的非图片文件应被拒绝"""
    response = client.post(
        "/api/admin/upload",
        files={"file": ("fake.jpg", b"this is not an image", "image/jpeg")},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400
    assert "不是有效的" in response.json()["detail"]


def test_upload_accepts_png(client: TestClient, auth_token: str, tmp_path, monkeypatch):
    """合法 PNG 文件可正常上传"""
    from app.utils import upload as upload_module

    monkeypatch.setattr(upload_module.settings, "UPLOAD_DIR", str(tmp_path))

    response = client.post(
        "/api/admin/upload",
        files={"file": ("cover.png", b"\x89PNG\r\n\x1a\n" + b"0" * 32, "image/png")},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    url = response.json()["url"]
    assert url.startswith("/static/uploads/")
    assert url.endswith(".png")
    assert len(list(tmp_path.glob("*.png"))) == 1
