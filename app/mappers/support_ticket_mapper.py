from data_models.support_ticket_data_model import SupportTicket
from models.support_ticket_model import (
    SupportTicketModel,
    SupportTicketListItemModel,
    SupportTicketsListModel,
    TicketUserInfoModel,
)
from mappers.support_message_mapper import SupportMessageMapper


class SupportTicketMapper:
    @staticmethod
    def to_model(ticket: SupportTicket) -> SupportTicketModel:
        return SupportTicketModel(
            id=ticket.id,
            user_id=ticket.user_id,
            status=ticket.status,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at,
            messages=[SupportMessageMapper.to_model(m) for m in ticket.messages],
        )

    @staticmethod
    def to_list_item(ticket: SupportTicket, last_message: str = None, last_message_at=None, message_count: int = 0) -> SupportTicketListItemModel:
        user = ticket.user
        return SupportTicketListItemModel(
            id=ticket.id,
            user_id=ticket.user_id,
            user=TicketUserInfoModel(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
            ),
            status=ticket.status,
            last_message=last_message,
            last_message_at=last_message_at,
            message_count=message_count,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at,
        )

    @staticmethod
    def to_list_model(tickets: list[SupportTicket], total: int, page: int, size: int,
                      extra: dict = None) -> SupportTicketsListModel:
        """
        `extra` — optional dict mapping ticket_id -> {last_message, last_message_at, message_count}
        """
        pages = (total + size - 1) // size
        items = []
        for ticket in tickets:
            info = extra.get(ticket.id, {}) if extra else {}
            items.append(SupportTicketMapper.to_list_item(
                ticket,
                last_message=info.get("last_message"),
                last_message_at=info.get("last_message_at"),
                message_count=info.get("message_count", len(ticket.messages)),
            ))
        return SupportTicketsListModel(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
        )
