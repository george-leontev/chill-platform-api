from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from data_models.support_ticket_data_model import SupportTicket, SupportMessage
from data_models.user_data_model import User


class SupportTicketRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_open_by_user_id(self, user_id: int) -> SupportTicket | None:
        return (
            self.db_session.query(SupportTicket)
            .filter(SupportTicket.user_id == user_id, SupportTicket.status == "open")
            .first()
        )

    def get_by_id(self, ticket_id: int) -> SupportTicket | None:
        return (
            self.db_session.query(SupportTicket)
            .options(joinedload(SupportTicket.user), joinedload(SupportTicket.messages))
            .filter(SupportTicket.id == ticket_id)
            .first()
        )

    def get_open_tickets(self, page: int, size: int) -> tuple[list[SupportTicket], int]:
        query = (
            self.db_session.query(SupportTicket)
            .options(joinedload(SupportTicket.user), joinedload(SupportTicket.messages))
            .filter(SupportTicket.status == "open")
        )
        total = query.count()
        tickets = query.order_by(SupportTicket.updated_at.desc()).offset((page - 1) * size).limit(size).all()
        return tickets, total

    def create(self, user_id: int) -> SupportTicket:
        ticket = SupportTicket(user_id=user_id, status="open")
        self.db_session.add(ticket)
        self.db_session.commit()
        self.db_session.refresh(ticket)
        return ticket

    def close(self, ticket: SupportTicket) -> SupportTicket:
        ticket.status = "closed"
        self.db_session.commit()
        self.db_session.refresh(ticket)
        return ticket


class SupportMessageRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_ticket_id(self, ticket_id: int, page: int, size: int) -> tuple[list[SupportMessage], int]:
        query = (
            self.db_session.query(SupportMessage)
            .filter(SupportMessage.ticket_id == ticket_id)
        )
        total = query.count()
        messages = query.order_by(SupportMessage.created_at.desc()).offset((page - 1) * size).limit(size).all()
        return messages, total

    def create(self, ticket_id: int, sender_id: int, content: str, is_from_support: bool = False) -> SupportMessage:
        message = SupportMessage(
            ticket_id=ticket_id,
            sender_id=sender_id,
            content=content,
            is_from_support=is_from_support,
        )
        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)
        return message
