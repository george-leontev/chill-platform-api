from typing import List
from models.app_base_model import AppBaseModel
from models.enums.user_role_enum import UserRoleEnum


class UserModel(AppBaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    role_id: UserRoleEnum

class UsersModel(AppBaseModel):
    items: List[UserModel]
    total: int
    page: int
    size: int
    pages: int

class PatchUserRoleModel(AppBaseModel):
    role_id: UserRoleEnum
