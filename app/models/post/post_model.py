from datetime import datetime
from typing import List
from models.user_info_model import UserInfoModel
from models.post.post_like_info_model import PostLikeInfoModel
from models.app_base_model import AppBaseModel
from models.post_image_model import PostImageModel


class PostModel(AppBaseModel):
    id: int

    title: str

    content: str

    created_at: datetime

    author: UserInfoModel

    images: List[PostImageModel] = []

    is_liked: bool = False

    likes: List[PostLikeInfoModel] = []

    likes_count: int = 0

class PostsModel(AppBaseModel):
    items: List[PostModel]
    total: int
    page: int
    size: int
    pages: int
