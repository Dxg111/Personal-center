from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Profile
from app.schemas import ProfileResponse

router = APIRouter(prefix="/api/profile", tags=["个人信息（公开）"])


@router.get("", response_model=ProfileResponse)
def get_profile(session: Session = Depends(get_session)):
    """获取个人信息"""
    statement = select(Profile).limit(1)
    profile = session.exec(statement).first()

    if not profile:
        raise HTTPException(status_code=404, detail="个人信息未配置")

    return profile
