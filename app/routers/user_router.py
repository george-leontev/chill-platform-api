from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models.enums.user_role_enum import UserRoleEnum
from utils.auth_helper import authorize
from models.user_model import UserModel, UsersModel, PatchUserRoleModel
from models.stats_model import StatsModel
from repositories.user_repository import UserRepository
from services.user_service import UserService

router = APIRouter()

def get_user_service(db_session: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db_session))

@router.get('/users', response_model=UsersModel)
async def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user = Depends(authorize([UserRoleEnum.MODERATOR])),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.get_paginated_users(page, size)

@router.patch('/users/{user_id}/role', response_model=UserModel)
async def update_user_role(
    user_id: int,
    body: PatchUserRoleModel,
    current_user = Depends(authorize([UserRoleEnum.MODERATOR])),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.update_role(user_id, body.role_id)

@router.get('/stats', response_model=StatsModel)
async def get_stats(
    current_user = Depends(authorize([UserRoleEnum.MODERATOR])),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.get_stats()

@router.get('/users/search', response_model=list[UserModel])
async def search_users(
    q: str = Query(..., min_length=1, max_length=100),
    current_user = Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER])),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.search_users(q)
