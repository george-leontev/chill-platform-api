from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from database import get_db
from data_models.user_data_model import User
from models.enums.user_role_enum import UserRoleEnum
from models.support_ticket_model import (
    SupportTicketModel,
    SupportMessageModel,
    SupportTicketsListModel,
    SupportMessageListModel,
    CreateSupportMessageModel,
)
from repositories.support_ticket_repository import SupportTicketRepository, SupportMessageRepository
from services.support_ticket_service import SupportTicketService
from utils.auth_helper import authorize, verify_token_from_string
from websocket.connection_manager import manager

router = APIRouter()


def get_support_service(db_session: Session = Depends(get_db)) -> SupportTicketService:
    return SupportTicketService(
        ticket_repo=SupportTicketRepository(db_session),
        message_repo=SupportMessageRepository(db_session),
    )


# ===================== User endpoints =====================


@router.get("/support/ticket", response_model=SupportTicketModel)
async def get_or_create_ticket(
    current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
    service: SupportTicketService = Depends(get_support_service),
):
    """Получить (или создать) свой активный тикет с сообщениями."""
    return service.get_or_create_ticket(current_user.id)


@router.post("/support/ticket/message", response_model=SupportMessageModel)
async def send_user_message(
    body: CreateSupportMessageModel,
    current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
    service: SupportTicketService = Depends(get_support_service),
):
    """Отправить сообщение в свой тикет."""
    message = service.send_user_message(current_user.id, body.content)

    # Notify all moderators via WebSocket
    await manager.broadcast(
        {
            "type": "support_message",
            "data": {
                "ticket_id": message.ticket_id,
                "user_id": current_user.id,
                "content": message.content,
                "message": message.model_dump(by_alias=True),
            },
        },
        exclude_user_id=current_user.id,
    )

    return message


# ===================== Admin endpoints =====================


@router.get("/support/tickets", response_model=SupportTicketsListModel)
async def get_open_tickets(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(authorize([UserRoleEnum.MODERATOR])),
    service: SupportTicketService = Depends(get_support_service),
):
    """Список всех открытых тикетов (для админа)."""
    return service.get_open_tickets(page, size)


@router.get("/support/tickets/{ticket_id}/messages", response_model=SupportMessageListModel)
async def get_ticket_messages(
    ticket_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    current_user: User = Depends(authorize([UserRoleEnum.MODERATOR])),
    service: SupportTicketService = Depends(get_support_service),
):
    """Сообщения конкретного тикета."""
    return service.get_ticket_messages(ticket_id, page, size)


@router.post("/support/tickets/{ticket_id}/reply", response_model=SupportMessageModel)
async def admin_reply(
    ticket_id: int,
    body: CreateSupportMessageModel,
    current_user: User = Depends(authorize([UserRoleEnum.MODERATOR])),
    service: SupportTicketService = Depends(get_support_service),
):
    """Ответ админа в тикет."""
    message = service.send_support_reply(ticket_id, current_user.id, body.content)

    # Notify the ticket owner via WebSocket
    ticket = service.ticket_repo.get_by_id(ticket_id)
    if ticket:
        await manager.send_to_user(ticket.user_id, {
            "type": "support_reply",
            "data": {
                "ticket_id": ticket_id,
                "message": message.model_dump(by_alias=True),
            },
        })

    return message


@router.put("/support/tickets/{ticket_id}/close", response_model=SupportTicketModel)
async def close_ticket(
    ticket_id: int,
    current_user: User = Depends(authorize([UserRoleEnum.MODERATOR])),
    service: SupportTicketService = Depends(get_support_service),
):
    """Закрыть тикет."""
    ticket = service.close_ticket(ticket_id)

    # Notify the ticket owner
    await manager.send_to_user(ticket.user_id, {
        "type": "support_ticket_closed",
        "data": {
            "ticket_id": ticket_id,
        },
    })

    return ticket


# ===================== WebSocket =====================


@router.websocket("/ws/support")
async def websocket_support(
    websocket: WebSocket,
    token: str,
    db_session: Session = Depends(get_db),
):
    """WebSocket для реалтайм-уведомлений поддержки."""
    try:
        payload = verify_token_from_string(token)
    except Exception as e:
        await websocket.close(code=4001, reason=str(e))
        return

    user_id = payload.get("user_id")
    if not user_id:
        await websocket.close(code=4002, reason="Invalid token payload")
        return

    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            # Currently handled server-side via REST endpoints;
            # this loop keeps the connection alive and can be extended.
    except WebSocketDisconnect:
        manager.disconnect(user_id)
