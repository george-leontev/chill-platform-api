from datetime import datetime
from typing import List, Optional

from models.app_base_model import AppBaseModel


class PartnerInfo(AppBaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    avatar: Optional[str] = None


class ConversationModel(AppBaseModel):
    partner: PartnerInfo

    last_message: str

    last_message_at: datetime

    unread_count: int


class ConversationsModel(AppBaseModel):
    items: List[ConversationModel]