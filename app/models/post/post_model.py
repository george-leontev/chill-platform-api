from typing import List
from models.app_base_model import AppBaseModel


class PostModel(AppBaseModel):
    id: int

    title: str

    content: str

    user_id: int

class PostsModel(AppBaseModel):
    items: List[PostModel]
