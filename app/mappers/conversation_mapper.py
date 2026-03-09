from models.conversation_model import ConversationModel, ConversationsModel

class ConversationMapper:
    @staticmethod
    def to_conversation_model(row) -> ConversationModel:
        result = ConversationModel(
            partner_id=row.partner_id,
            last_message=row.last_message,
            last_message_at=row.last_message_at,
            unread_count=row.unread_count
        )

        return result

    @staticmethod
    def to_conversations_model(rows) -> ConversationsModel:
        result = ConversationsModel(
            items=[ConversationMapper.to_conversation_model(row) for row in rows]
        )

        return result