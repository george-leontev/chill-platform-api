from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from data_models.user_data_model import User
from models.enums.user_role_enum import UserRoleEnum
from models.profile_model import ProfileModel, CreateOrUpdateProfileModel
from repositories.profile_repository import ProfileRepository
from services.profile_service import ProfileService
from utils.auth_helper import authorize

router = APIRouter()


def get_profile_service(db_session: Session = Depends(get_db)) -> ProfileService:
    return ProfileService(
        profile_repository=ProfileRepository(db_session)
    )


@router.get("/profile", response_model=ProfileModel)
async def get_profile(
    current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
    profile_service: ProfileService = Depends(get_profile_service)
):
    profile = profile_service.get_profile(current_user.id)

    return profile


@router.get("/profile/{user_id}", response_model=ProfileModel)
async def get_profile_by_user_id(
    user_id: int,
    current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
    profile_service: ProfileService = Depends(get_profile_service)
):
    profile = profile_service.get_profile(user_id)

    return profile


@router.post("/profile", response_model=ProfileModel)
async def create_profile(
    profile_data: CreateOrUpdateProfileModel,
    current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
    profile_service: ProfileService = Depends(get_profile_service)
):
    profile = profile_service.create_profile(current_user.id, profile_data)

    return profile


@router.put("/profile", response_model=ProfileModel)
async def update_profile(
    profile_data: CreateOrUpdateProfileModel,
    current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
    profile_service: ProfileService = Depends(get_profile_service)
):
    profile = profile_service.update_profile(current_user.id, profile_data)

    return profile


@router.delete("/profile", response_model=ProfileModel)
async def delete_profile(
    current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
    profile_service: ProfileService = Depends(get_profile_service)
):
    profile = profile_service.delete_profile(current_user.id)

    return profile
