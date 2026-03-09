from datetime import datetime
from typing import List
from models.enums.friend_status_enum import FriendStatusEnum
from models.app_base_model import AppBaseModel


class FriendModel(AppBaseModel):
    id: int

    user_id: int

    friend_id: int

    status_id: FriendStatusEnum

    created_at: datetime

class FriendsModel(AppBaseModel):
    items: List[FriendModel]
