from http import HTTPStatus
from fastapi import HTTPException
from mappers.conversation_mapper import ConversationMapper
from models.conversation_model import ConversationsModel
from mappers.message_mapper import MessageMapper
from models.message_model import MessageModel, MessagesModel
from repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository
        self.message_mapper = MessageMapper()
        self.conversation_mapper = ConversationMapper()

    def create(self, sender_id: int, receiver_id: int, content: str) -> MessageModel:
        if sender_id == receiver_id:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Нельзя отправить сообщение себе.')

        message = self.message_repository.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )

        result = self.message_mapper.to_model(message)

        return result

    def mark_as_read(self, user_id: int, sender_id: int) -> None:
        if not user_id or not sender_id:
            return

        self.message_repository.mark_as_read(user_id, sender_id)

    def get_conversation(self, user_id: int, other_user_id: int, limit: int = 50, offset: int = 0) -> MessagesModel:
        messages = self.message_repository.get_conversation(user_id, other_user_id, limit, offset)

        result = self.message_mapper.to_list_model(messages)

        return result

    def get_conversations(self, user_id: int) -> ConversationsModel:
        conversations = self.message_repository.get_conversations(user_id)

        result = self.conversation_mapper.to_conversations_model(conversations)

        return result
