from data_models.support_ticket_data_model import SupportMessage
from models.support_ticket_model import SupportMessageModel, SupportMessageListModel


class SupportMessageMapper:
    @staticmethod
    def to_model(message: SupportMessage) -> SupportMessageModel:
        return SupportMessageModel(
            id=message.id,
            ticket_id=message.ticket_id,
            sender_id=message.sender_id,
            content=message.content,
            is_from_support=message.is_from_support,
            created_at=message.created_at,
        )

    @staticmethod
    def to_list_model(messages: list[SupportMessage], total: int, page: int, size: int) -> SupportMessageListModel:
        pages = (total + size - 1) // size
        return SupportMessageListModel(
            items=[SupportMessageMapper.to_model(m) for m in messages],
            total=total,
            page=page,
            size=size,
            pages=pages,
        )
