from datetime import datetime
from typing import List, Optional
from models.app_base_model import AppBaseModel


class SupportMessageModel(AppBaseModel):
    id: int
    ticket_id: int
    sender_id: int
    content: str
    is_from_support: bool
    created_at: datetime


class SupportMessageListModel(AppBaseModel):
    items: List[SupportMessageModel]
    total: int
    page: int
    size: int
    pages: int


class TicketUserInfoModel(AppBaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str


class SupportTicketListItemModel(AppBaseModel):
    id: int
    user_id: int
    user: TicketUserInfoModel
    status: str
    last_message: Optional[str] = None
    last_message_at: Optional[datetime] = None
    message_count: int
    created_at: datetime
    updated_at: datetime


class SupportTicketsListModel(AppBaseModel):
    items: List[SupportTicketListItemModel]
    total: int
    page: int
    size: int
    pages: int


class SupportTicketModel(AppBaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    messages: List[SupportMessageModel]


class CreateSupportMessageModel(AppBaseModel):
    content: str


class CloseTicketModel(AppBaseModel):
    ticket_id: int
    status: str
