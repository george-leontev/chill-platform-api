from datetime import datetime
from typing import Optional
from models.app_base_model import AppBaseModel
from models.user_info_model import UserInfoModel


class ProfileModel(AppBaseModel):
    id: int
    user_id: int
    user: Optional[UserInfoModel] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class UserInfoInputModel(AppBaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class CreateOrUpdateProfileModel(AppBaseModel):
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[str] = None
    user: Optional[UserInfoInputModel] = None
