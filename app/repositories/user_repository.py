from sqlalchemy.orm import Session
from sqlalchemy import func
from data_models.user_data_model import User
from data_models.post_data_model import Post
from data_models.message_data_model import Message
from data_models.friend_data_model import Friend
from models.enums.user_role_enum import UserRoleEnum

class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, user_id: int) -> User | None:
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_paginated_users(self, page: int, size: int) -> tuple[list[User], int]:
        query = self.db_session.query(User)
        total = query.count()
        users = query.offset((page - 1) * size).limit(size).all()
        return users, total

    def update_role(self, user: User, role_id: UserRoleEnum) -> User:
        user.role_id = role_id
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_stats(self) -> dict:
        users_count = self.db_session.query(func.count(User.id)).scalar()
        posts_count = self.db_session.query(func.count(Post.id)).scalar()
        messages_count = self.db_session.query(func.count(Message.id)).scalar()
        friends_count = self.db_session.query(func.count(Friend.id)).scalar()

        return {
            "users_count": users_count,
            "posts_count": posts_count,
            "messages_count": messages_count,
            "friends_count": friends_count
        }
