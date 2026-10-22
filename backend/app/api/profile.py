from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Profile
from app.schemas import ProfileResponse
import json

router = APIRouter(prefix="/api/profile", tags=["个人信息（公开）"])


@router.get("", response_model=ProfileResponse)
def get_profile(session: Session = Depends(get_session)):
    """获取个人信息"""
    statement = select(Profile).limit(1)
    profile = session.exec(statement).first()

    if not profile:
        raise HTTPException(status_code=404, detail="个人信息未配置")

    # BUG-11 修复：解析雷达图技能JSON
    profile_dict = profile.model_dump()
    if profile.radar_skills:
        try:
            profile_dict['radar_skills'] = json.loads(profile.radar_skills)
        except:
            profile_dict['radar_skills'] = None

    return ProfileResponse(**profile_dict)
