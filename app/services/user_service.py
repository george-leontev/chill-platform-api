from http import HTTPStatus
from fastapi import HTTPException
from repositories.user_repository import UserRepository
from mappers.user_mapper import UserMapper
from models.user_model import UserModel, UsersModel
from models.stats_model import StatsModel
from models.enums.user_role_enum import UserRoleEnum

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.mapper = UserMapper()

    def get_paginated_users(self, page: int, size: int) -> UsersModel:
        users, total = self.user_repository.get_paginated_users(page, size)
        return self.mapper.to_paginated_model(users, total, page, size)

    def update_role(self, user_id: int, role_id: UserRoleEnum) -> UserModel:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Пользователь не найден.")

        updated_user = self.user_repository.update_role(user, role_id)
        return self.mapper.to_model(updated_user)

    def get_stats(self) -> StatsModel:
        stats = self.user_repository.get_stats()
        return StatsModel(**stats)

    def search_users(self, query: str) -> list[UserModel]:
        """Search users by username, first_name, or last_name"""
        users = self.user_repository.search_users(query)
        return [self.mapper.to_model(user) for user in users]
