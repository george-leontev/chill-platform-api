import os
import uuid
from http import HTTPStatus
from fastapi import HTTPException, UploadFile
from mappers.post_mapper import PostMapper
from models.post.post_model import PostModel, PostsModel
from models.post_like_model import PostLikeModel
from data_models.post_data_model import Post
from data_models.post_likes_data_model import PostLike
from data_models.user_data_model import User
from models.enums.user_role_enum import UserRoleEnum
from repositories.post_repository import PostRepository
from repositories.post_like_repository import PostLikeRepository


class PostService:
    def __init__(self, post_repository: PostRepository, like_repository: PostLikeRepository):
        self.post_repository = post_repository
        self.like_repository = like_repository
        self.mapper = PostMapper()
        self.upload_dir = "app/uploads/posts"

    def _save_image(self, file: UploadFile) -> str:
        """Save uploaded image and return its URL path"""
        os.makedirs(self.upload_dir, exist_ok=True)

        # Generate unique filename
        file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(self.upload_dir, unique_filename)

        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Return URL path (relative to static files)
        return f"/uploads/posts/{unique_filename}"

    def get_all(self, current_user_id: int = None) -> PostsModel:
        posts = self.post_repository.get_all()

        result = self.mapper.to_list_model(posts, current_user_id)

        return result

    def get_by_id(self, post_id: int, current_user_id: int = None) -> PostModel:
        post = self.post_repository.get_by_id(post_id)

        if not post:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Публикация не найдена.')

        result = self.mapper.to_model(post, current_user_id)

        return result

    def get_my_posts(self, user_id: int) -> PostsModel:
        posts = self.post_repository.get_by_user_id(user_id)

        result = self.mapper.to_list_model(posts, user_id)

        return result

    def get_liked_posts(self, user_id: int) -> PostsModel:
        posts = self.like_repository.get_liked_posts(user_id)

        result = self.mapper.to_list_model(posts, user_id)

        return result

    def create(self, title: str, content: str, current_user: User, images: list[str] = None) -> PostModel:
        image_urls = images or []

        post = self.post_repository.create(title=title, content=content, user_id=current_user.id, image_urls=image_urls)

        result = self.mapper.to_model(post, current_user.id)

        return result

    def update(self, post_id: int, title: str, content: str, current_user: User, images: list[str] = None) -> PostModel:
        post = self.post_repository.get_by_id(post_id)

        if not post:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Публикация не найдена.')

        self._check_ownership(post.user_id, current_user, action='редактирования')

        image_urls = images
        if images is None:
            image_urls = None  # Keep existing images

        updated_post = self.post_repository.update(post, title=title, content=content, image_urls=image_urls)

        result = self.mapper.to_model(updated_post, current_user.id)

        return result

    def delete(self, post_id: int, current_user: User) -> PostModel:
        post = self.post_repository.get_by_id(post_id)

        if not post:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Публикация не найдена.')

        self._check_ownership(post.user_id, current_user, action='удаления')

        deleted_post = self.post_repository.delete(post)

        result = self.mapper.to_model(deleted_post, current_user.id)

        return result

    def toggle_like(self, post_id: int, current_user: User) -> PostLikeModel:
        post = self.post_repository.get_by_id(post_id)

        if not post:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Публикация не найдена.')

        existing = self.like_repository.get_like(user_id=current_user.id, post_id=post_id)

        if existing:
            like, like_count = self.like_repository.delete_like(existing)

            result = self.mapper.to_like_model(like, liked=False, like_count=like_count)
        else:
            like, like_count = self.like_repository.create_like(user_id=current_user.id, post_id=post_id)

            result = self.mapper.to_like_model(like, liked=True, like_count=like_count)

        return result

    def _check_ownership(self, owner_id: int, current_user: User, action: str):
        is_owner = owner_id == current_user.id
        is_moderator = UserRoleEnum(current_user.role_id) == UserRoleEnum.MODERATOR

        if not is_owner and not is_moderator:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail=f'Недостаточно прав для {action} этой публикации.'
            )
