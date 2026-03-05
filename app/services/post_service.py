from http import HTTPStatus
from fastapi import HTTPException
from models.post_like_model import PostLikeModel
from data_models.user_data_model import User
from models.enums.user_role_enum import UserRoleEnum
from repositories.post_repository import PostRepository
from repositories.post_like_repository import PostLikeRepository

class PostService:
    def __init__(self, post_repository: PostRepository, like_repository: PostLikeRepository):
        self.post_repository = post_repository
        self.like_repository = like_repository

    def get_all(self):
        return self.post_repository.get_all()

    def get_by_id(self, post_id: int):
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Публикация не найдена.')

        return post

    def get_my_posts(self, user_id: int):
        return self.post_repository.get_by_user_id(user_id)

    def create(self, title: str, content: str, current_user: User):
        return self.post_repository.create(title=title, content=content, user_id=current_user.id)

    def update(self, post_id: int, title: str, content: str, current_user: User):
        post = self.get_by_id(post_id)
        self._check_ownership(post.user_id, current_user, action='редактирования')

        return self.post_repository.update(post, title=title, content=content)

    def delete(self, post_id: int, current_user: User):
        post = self.get_by_id(post_id)
        self._check_ownership(post.user_id, current_user, action='удаления')

        return self.post_repository.delete(post)

    def toggle_like(self, post_id: int, current_user: User):
        self.get_by_id(post_id)
        existing = self.like_repository.get_like(user_id=current_user.id, post_id=post_id)

        if existing:
            like = self.like_repository.delete_like(existing)

            return PostLikeModel(
                user_id=like.user_id,
                post_id=like.post_id,
                liked=False
            )
        else:
            like = self.like_repository.create_like(user_id=current_user.id, post_id=post_id)

            return PostLikeModel(
                user_id=like.user_id,
                post_id=like.post_id,
                liked=False
            )

    def _check_ownership(self, owner_id: int, current_user: User, action: str):
        is_owner = owner_id == current_user.id
        is_moderator = UserRoleEnum(current_user.role_id) == UserRoleEnum.MODERATOR
        if not is_owner and not is_moderator:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail=f'Недостаточно прав для {action} этой публикации.'
            )