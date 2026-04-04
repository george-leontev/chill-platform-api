from fastapi import HTTPException

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from models.conversation_model import ConversationsModel
from database import get_db
from data_models.user_data_model import User
from models.enums.user_role_enum import UserRoleEnum
from models.message_model import MessagesModel
from repositories.message_repository import MessageRepository
from services.message_service import MessageService
from utils.auth_helper import authorize, verify_token_from_string
from websocket.connection_manager import manager

router = APIRouter()


def get_message_service(db_session: Session = Depends(get_db)) -> MessageService:
    return MessageService(
        message_repository=MessageRepository(db_session)
    )

@router.get('/messages/conversations', response_model=ConversationsModel)
async def get_conversations(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
        service: MessageService = Depends(get_message_service)
    ):
    conversations = service.get_conversations(current_user.id, page, size)

    return conversations

@router.get('/messages/{user_id}', response_model=MessagesModel)
async def get_conversation(
        user_id: int,
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
        service: MessageService = Depends(get_message_service)
    ):
    messages = service.get_conversation(current_user.id, user_id, page, size)

    return messages

@router.put('/messages/{user_id}/read')
async def mark_as_read(
        user_id: int,
        current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
        service: MessageService = Depends(get_message_service)
    ):
    service.mark_as_read(current_user.id, user_id)

    return {"detail": "Сообщения прочитаны."}

@router.get('/users/{user_id}/online', dependencies=[Depends(authorize([UserRoleEnum.MODERATOR, UserRoleEnum.USER]))])
async def get_online_status(user_id: int):
    online = manager.is_online(user_id)

    return {"user_id": user_id, "online": online}

@router.websocket('/ws/messages')
async def websocket_messages(
        websocket: WebSocket,
        token: str,
        db_session: Session = Depends(get_db)
    ):
    print("WebSocket connection attempt with token:", token)

    try:
        payload = verify_token_from_string(token)
    except HTTPException as e:
        print(f"Token verification failed: {e.detail}")
        await websocket.close(code=4001, reason=e.detail)
        return

    current_user_id = payload.get("user_id")

    if not current_user_id:
        await websocket.close(code=4002, reason="Invalid token payload")
        return

    await manager.connect(current_user_id, websocket)

    try:
        service = MessageService(MessageRepository(db_session))

        while True:
            data = await websocket.receive_json()

            event_type = data.get("type")
            print(f"event_type: {event_type}")

            # -- new message --
            if event_type == "new_message":
                print(f"Received message data: {data}")
                receiver_id = data.get("receiverId") or data.get("receiver_id")
                content = data.get("content")

                if not receiver_id:
                    await websocket.send_json({
                        "type": "error",
                        "data": {"message": "receiverId is required"}
                    })
                    continue

                message = service.create(
                    sender_id=current_user_id,
                    receiver_id=receiver_id,
                    content=content
                )

                payload = {
                    "type": "new_message",
                    "data": message.model_dump(by_alias=True)
                }

                await manager.send_to_user(receiver_id, payload)
                await manager.send_to_user(current_user_id, payload)

            elif event_type == "read":
                sender_id = data.get("sender_id")
                print(f"herererer sender_id = {sender_id}")
                if not sender_id:
                    continue

                service.mark_as_read(current_user_id, sender_id)

                # notify sender their messages were read
                await manager.send_to_user(sender_id, {
                    "type": "read",
                    "data": {
                        "byUserId": current_user_id
                    }
                })

            # -- typing indicator --
            elif event_type == "typing":
                receiver_id = data.get("receiver_id")
                is_typing = data.get("is_typing", True)

                await manager.send_to_user(receiver_id, {
                    "type": "typing",
                    "data": {
                        "user_id": current_user_id,
                        "is_typing": is_typing
                    }
                })

    except WebSocketDisconnect:
        manager.disconnect(current_user_id)

        # notify all active connections that user went offline
        await manager.broadcast({"type": "user_offline", "userId": current_user_id})
        