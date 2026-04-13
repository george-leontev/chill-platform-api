from http import HTTPStatus
from fastapi import HTTPException
from mappers.support_message_mapper import SupportMessageMapper
from mappers.support_ticket_mapper import SupportTicketMapper
from models.support_ticket_model import (
    SupportTicketModel,
    SupportMessageModel,
    SupportTicketsListModel,
    SupportMessageListModel,
)
from repositories.support_ticket_repository import SupportTicketRepository, SupportMessageRepository


class SupportTicketService:
    def __init__(
        self,
        ticket_repo: SupportTicketRepository,
        message_repo: SupportMessageRepository,
    ):
        self.ticket_repo = ticket_repo
        self.message_repo = message_repo
        self.ticket_mapper = SupportTicketMapper()
        self.message_mapper = SupportMessageMapper()

    # -- User-facing --

    def get_or_create_ticket(self, user_id: int) -> SupportTicketModel:
        ticket = self.ticket_repo.get_open_by_user_id(user_id)
        if not ticket:
            ticket = self.ticket_repo.create(user_id)
        return self.ticket_mapper.to_model(ticket)

    def send_user_message(self, user_id: int, content: str) -> SupportMessageModel:
        ticket = self.ticket_repo.get_open_by_user_id(user_id)
        if not ticket:
            ticket = self.ticket_repo.create(user_id)

        message = self.message_repo.create(
            ticket_id=ticket.id,
            sender_id=user_id,
            content=content,
            is_from_support=False,
        )
        return self.message_mapper.to_model(message)

    # -- Admin-facing --

    def get_open_tickets(self, page: int, size: int) -> SupportTicketsListModel:
        tickets, total = self.ticket_repo.get_open_tickets(page, size)

        # Build extra info: last message, last_message_at, message_count per ticket
        extra = {}
        for ticket in tickets:
            msgs = ticket.messages
            if msgs:
                last_msg = msgs[-1]
                extra[ticket.id] = {
                    "last_message": last_msg.content,
                    "last_message_at": last_msg.created_at,
                    "message_count": len(msgs),
                }
            else:
                extra[ticket.id] = {"message_count": 0}

        return self.ticket_mapper.to_list_model(tickets, total, page, size, extra=extra)

    def get_ticket_messages(self, ticket_id: int, page: int, size: int) -> SupportMessageListModel:
        ticket = self.ticket_repo.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Тикет не найден.")

        messages, total = self.message_repo.get_by_ticket_id(ticket_id, page, size)
        return self.message_mapper.to_list_model(messages, total, page, size)

    def send_support_reply(self, ticket_id: int, admin_id: int, content: str) -> SupportMessageModel:
        ticket = self.ticket_repo.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Тикет не найден.")
        if ticket.status == "closed":
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Тикет закрыт.")

        message = self.message_repo.create(
            ticket_id=ticket_id,
            sender_id=admin_id,
            content=content,
            is_from_support=True,
        )
        return self.message_mapper.to_model(message)

    def close_ticket(self, ticket_id: int) -> SupportTicketModel:
        ticket = self.ticket_repo.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Тикет не найден.")
        if ticket.status == "closed":
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Тикет уже закрыт.")

        ticket = self.ticket_repo.close(ticket)
        return self.ticket_mapper.to_model(ticket)
