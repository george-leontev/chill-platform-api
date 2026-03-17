from datetime import datetime
from models.app_base_model import AppBaseModel


class PostLikeInfoModel(AppBaseModel):
    user_id: int

    created_at: datetime
