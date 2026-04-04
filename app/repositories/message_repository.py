from sqlalchemy import case, func, or_, select
from sqlalchemy.orm import Session
from data_models.message_data_model import Message
from data_models.user_data_model import User


class MessageRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_conversation(
        self,
        user_id: int,
        other_user_id: int,
        page: int,
        size: int
    ) -> tuple[list[Message], int]:
        query = self.db_session.query(Message).filter(or_(
            (Message.sender_id == user_id) & (Message.receiver_id == other_user_id),
            (Message.sender_id == other_user_id) & (Message.receiver_id == user_id)
        ))
        total = query.count()
        messages = query.order_by(Message.created_at.desc()).offset((page - 1) * size).limit(size).all()

        return messages, total

    def create(self, sender_id: int, receiver_id: int, content: str) -> Message:
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )

        self.db_session.add(message)
        self.db_session.commit()

        return message

    def mark_as_read(self, user_id: int, sender_id: int) -> None:
        self.db_session.query(Message).filter(
            Message.receiver_id == user_id,
            Message.sender_id == sender_id,
            Message.is_read == False
        ).update({"is_read": True})

        self.db_session.commit()

    def get_conversations(self, user_id: int, page: int, size: int) -> tuple[list, int]:
        partner_id_case = case(
            (Message.sender_id == user_id, Message.receiver_id),
            else_=Message.sender_id
        )

        # Subquery to get the last message content for each conversation
        last_message_subquery = (
            select(Message.content)
            .where(
                or_(
                    (Message.sender_id == user_id) & (Message.receiver_id == partner_id_case),
                    (Message.sender_id == partner_id_case) & (Message.receiver_id == user_id)
                )
            )
            .order_by(Message.created_at.desc())
            .limit(1)
            .correlate()
            .scalar_subquery()
        )

        query = self.db_session.query(
            partner_id_case.label("partner_id"),
            User.id.label("partner_user_id"),
            User.username.label("partner_username"),
            User.first_name.label("partner_first_name"),
            User.last_name.label("partner_last_name"),
            func.max(Message.created_at).label("last_message_at"),
            last_message_subquery.label("last_message"),
            func.count(
                case((
                    (Message.receiver_id == user_id) & (Message.is_read == False), 1
                ))
            ).label("unread_count")
        ).join(
            User, User.id == partner_id_case
        ).filter(
            or_(Message.sender_id == user_id, Message.receiver_id == user_id)
        ).group_by(
            partner_id_case,
            User.id,
            User.username,
            User.first_name,
            User.last_name
        )
        
        # To get total count of conversations, we need to count the groups
        total = self.db_session.query(partner_id_case).filter(
            or_(Message.sender_id == user_id, Message.receiver_id == user_id)
        ).distinct().count()

        conversations = query.order_by(func.max(Message.created_at).desc()).offset((page - 1) * size).limit(size).all()

        return conversations, total
