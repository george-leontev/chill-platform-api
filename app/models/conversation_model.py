from datetime import datetime
from typing import List

from models.app_base_model import AppBaseModel


class ConversationModel(AppBaseModel):
    partner_id: int

    last_message: str

    last_message_at: datetime

    unread_count: int

class ConversationsModel(AppBaseModel):
    items: List[ConversationModel]