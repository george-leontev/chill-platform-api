from models.conversation_model import ConversationModel, ConversationsModel, PartnerInfo

class ConversationMapper:
    @staticmethod
    def to_conversation_model(row) -> ConversationModel:
        partner_info = PartnerInfo(
            id=row.partner_user_id,
            username=row.partner_username,
            first_name=row.partner_first_name,
            last_name=row.partner_last_name
        )

        result = ConversationModel(
            partner=partner_info,
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