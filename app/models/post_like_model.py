from models.app_base_model import AppBaseModel


class PostLikeModel(AppBaseModel):
    user_id: int

    post_id: int

    liked: bool

    like_count: int
