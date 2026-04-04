from data_models.user_data_model import User
from models.user_model import UserModel, UsersModel
from models.enums.user_role_enum import UserRoleEnum

class UserMapper:
    @staticmethod
    def to_model(user: User) -> UserModel:
        return UserModel(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role_id=UserRoleEnum(user.role_id)
        )

    @staticmethod
    def to_paginated_model(users: list[User], total: int, page: int, size: int) -> UsersModel:
        pages = (total + size - 1) // size
        return UsersModel(
            items=[UserMapper.to_model(user) for user in users],
            total=total,
            page=page,
            size=size,
            pages=pages
        )
