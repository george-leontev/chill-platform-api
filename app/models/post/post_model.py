from datetime import datetime
from typing import List
from models.post.post_author_model import PostAuthorModel
from models.post.post_like_info_model import PostLikeInfoModel
from models.app_base_model import AppBaseModel
from models.post_image_model import PostImageModel


class PostModel(AppBaseModel):
    id: int

    title: str

    content: str

    created_at: datetime

    author: PostAuthorModel

    images: List[PostImageModel] = []

    is_liked: bool = False

    likes: List[PostLikeInfoModel] = []

    likes_count: int = 0

class PostsModel(AppBaseModel):
    items: List[PostModel]
