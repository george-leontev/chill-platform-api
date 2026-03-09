from http import HTTPStatus
from fastapi import HTTPException
from mappers.friend_mapper import FriendMapper
from models.enums.friend_status_enum import FriendStatusEnum
from models.friend_model import FriendModel, FriendsModel
from repositories.friend_repository import FriendRepository


class FriendService:
    def __init__(self, friend_repository: FriendRepository):
        self.friend_repository = friend_repository
        self.mapper = FriendMapper()

    def get_accepted_friends(self, user_id: int) -> FriendsModel:
        friends = self.friend_repository.get_accepted_friends(user_id)

        result = self.mapper.to_list_model(friends)

        return result

    def get_incoming_requests(self, user_id: int) -> FriendsModel:
        incoming = self.friend_repository.get_incoming_requests(user_id)

        result = self. mapper.to_list_model(incoming)

        return result

    def get_outgoing_requests(self, user_id: int) -> FriendsModel:
        outgoing = self.friend_repository.get_outgoing_requests(user_id)

        result = self.mapper.to_list_model(outgoing)

        return result

    def get(self, user_id: int, friend_id: int) -> FriendModel:
        friendship = self.friend_repository.get_friendship(user_id, friend_id)

        if not friendship:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Дружба не найдена.')

        result = self.mapper.to_model(friendship)

        return result

    def create(self, user_id: int, friend_id: int) -> FriendModel:
        if user_id == friend_id:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Нельзя добавить себя в друзья.')

        existing = self.friend_repository.get_friendship(user_id, friend_id)

        if existing:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Запрос уже существует или вы уже друзья.')

        friend_request = self.friend_repository.create_friendship(user_id, friend_id)

        result = self.mapper.to_model(friend_request)

        return result

    def accept(self, current_user_id: int, sender_id: int) -> FriendModel:
        friendship = self.friend_repository.get_friendship(current_user_id, sender_id)

        if not friendship:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Запрос на дружбу не найден.')

        if friendship.friend_id != current_user_id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Вы не можете принять свой собственный запрос.')

        if friendship.status_id != FriendStatusEnum.PENDING.value:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Запрос уже обработан.')

        updated = self.friend_repository.update_friendship_status(friendship, FriendStatusEnum.ACCEPTED.value)

        result = self.mapper.to_model(updated)

        return result

    def decline(self, current_user_id: int, sender_id: int) -> FriendModel:
        friendship = self.friend_repository.get_friendship(current_user_id, sender_id)

        if not friendship:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Запрос на дружбу не найден.')

        if friendship.friend_id != current_user_id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Вы не можете отклонить свой собственный запрос.')

        if friendship.status_id != FriendStatusEnum.PENDING.value:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Запрос уже обработан.')

        updated = self.friend_repository.update_friendship_status(friendship, FriendStatusEnum.DECLINED.value)

        result = self.mapper.to_model(updated)

        return result

    def delete(self, current_user_id: int, target_user_id: int) -> FriendModel:
        friendship = self.friend_repository.get_friendship(current_user_id, target_user_id)

        if not friendship:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Дружба не найдена.')

        if friendship.user_id != current_user_id and friendship.friend_id != current_user_id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Недостаточно прав.')

        deleted = self.friend_repository.delete_friendship(friendship)

        result = self.mapper.to_model(deleted)

        return result
