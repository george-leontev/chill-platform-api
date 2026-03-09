from sqlalchemy import case, func, or_
from sqlalchemy.orm import Session
from data_models.message_data_model import Message


class MessageRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_conversation(
        self,
        user_id: int,
        other_user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> list[Message]:
        messages = self.db_session.query(Message).filter(
            (Message.sender_id == user_id) & (Message.receiver_id == other_user_id) |
            (Message.sender_id == other_user_id) & (Message.receiver_id == user_id)
        ).order_by(Message.created_at.desc()).limit(limit).offset(offset).all()

        return messages

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

    def get_conversations(self, user_id: int) -> list:
        # get last message and unread count per conversation partner
        conversations = self.db_session.query(
            case(
                (Message.sender_id == user_id, Message.receiver_id),
                else_=Message.sender_id
            ).label("partner_id"),
            func.max(Message.created_at).label("last_message_at"),
            func.max(Message.content).label("last_message"),
            func.count(
                case((
                    (Message.receiver_id == user_id) & (Message.is_read == False), 1
                ))
            ).label("unread_count")
        ).filter(
            or_(Message.sender_id == user_id, Message.receiver_id == user_id)
        ).group_by(
            case(
                (Message.sender_id == user_id, Message.receiver_id),
                else_=Message.sender_id
            )
        ).order_by(func.max(Message.created_at).desc()).all()

        return conversations
