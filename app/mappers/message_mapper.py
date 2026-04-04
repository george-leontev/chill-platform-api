from data_models.message_data_model import Message
from models.message_model import MessageModel, MessagesModel


class MessageMapper:
    @staticmethod
    def to_model(message: Message) -> MessageModel:
        result = MessageModel(
            id=message.id,
            content=message.content,
            is_read=message.is_read,
            sender_id=message.sender_id,
            receiver_id=message.receiver_id,
            created_at=message.created_at
        )

        return result

    @staticmethod
    def to_list_model(messages: list[Message], total: int, page: int, size: int) -> MessagesModel:
        pages = (total + size - 1) // size
        result = MessagesModel(
            items=[MessageMapper.to_model(message) for message in messages],
            total=total,
            page=page,
            size=size,
            pages=pages
        )

        return result
