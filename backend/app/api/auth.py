from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import timedelta
from app.database import get_session
from app.schemas import LoginRequest, LoginResponse
from app.utils.auth import authenticate_user, create_access_token
from app.config import get_settings

router = APIRouter(prefix="/api/auth", tags=["认证"])
settings = get_settings()


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, session: Session = Depends(get_session)):
    """管理员登录"""
    user = authenticate_user(session, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return LoginResponse(access_token=access_token)
