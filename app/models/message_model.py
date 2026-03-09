from datetime import datetime
from typing import List
from models.app_base_model import AppBaseModel


class MessageModel(AppBaseModel):
    id: int

    content: str

    is_read: bool

    sender_id: int

    receiver_id: int
    
    created_at: datetime


class MessagesModel(AppBaseModel):
    items: List[MessageModel]
