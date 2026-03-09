from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from data_models.user_data_model import User
from models.enums.user_role_enum import UserRoleEnum
from models.friend_model import FriendModel, FriendsModel
from repositories.friend_repository import FriendRepository
from services.friend_service import FriendService
from utils.auth_helper import authorize

router = APIRouter()


def get_friend_service(db_session: Session = Depends(get_db)) -> FriendService:
    return FriendService(
        friend_repository=FriendRepository(db_session)
    )


@router.get('/friends', tags=['Friends'], response_model=FriendsModel)
async def get_accepted_friends(
        current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
        friend_service: FriendService = Depends(get_friend_service)
    ):
    friends = friend_service.get_accepted_friends(current_user.id)

    return friends


@router.get('/friends/requests/incoming', tags=['Friends'], response_model=FriendsModel)
async def get_incoming_requests(
        current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
        friend_service: FriendService = Depends(get_friend_service)
    ):
    incoming = friend_service.get_incoming_requests(current_user.id)

    return incoming


@router.get('/friends/requests/outgoing', tags=['Friends'], response_model=FriendsModel)
async def get_outgoing_requests(
        current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
        friend_service: FriendService = Depends(get_friend_service)
    ):
    outgoing = friend_service.get_outgoing_requests(current_user.id)

    return outgoing


@router.get('/friends/{user_id}/status', tags=['Friends'], response_model=FriendModel)
async def get_friendship_status(
        user_id: int,
        current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
        friend_service: FriendService = Depends(get_friend_service)
    ):
    friendship = friend_service.get(current_user.id, user_id)

    return friendship


@router.post('/friends/{user_id}', tags=['Friends'], response_model=FriendModel)
async def send_friend_request(
        user_id: int,
        current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
        friend_service: FriendService = Depends(get_friend_service)
    ):
    friend_request = friend_service.create(current_user.id, user_id)

    return friend_request


@router.put('/friends/{user_id}/accept', tags=['Friends'], response_model=FriendModel)
async def accept_friend_request(
        user_id: int,
        current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
        friend_service: FriendService = Depends(get_friend_service)
    ):
    accepted = friend_service.accept(current_user.id, user_id)

    return accepted


@router.put('/friends/{user_id}/decline', tags=['Friends'], response_model=FriendModel)
async def decline_friend_request(
        user_id: int,
        current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
        friend_service: FriendService = Depends(get_friend_service)
    ):
    declined = friend_service.decline(current_user.id, user_id)

    return declined


@router.delete('/friends/{user_id}', tags=['Friends'], response_model=FriendModel)
async def remove_friend(
        user_id: int,
        current_user: User = Depends(authorize([UserRoleEnum.USER, UserRoleEnum.MODERATOR])),
        friend_service: FriendService = Depends(get_friend_service)
    ):
    deleted = friend_service.delete(current_user.id, user_id)

    return deleted
