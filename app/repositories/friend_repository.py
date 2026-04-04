from sqlalchemy.orm import Session
from sqlalchemy import or_
from data_models.friend_data_model import Friend
from models.enums.friend_status_enum import FriendStatusEnum


class FriendRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_accepted_friends(self, user_id: int, page: int, size: int) -> tuple[list[Friend], int]:
        query = self.db_session.query(Friend).filter(
            or_(Friend.user_id == user_id, Friend.friend_id == user_id),
            Friend.status_id == FriendStatusEnum.ACCEPTED
        )
        total = query.count()
        friends = query.order_by(Friend.created_at.desc()).offset((page - 1) * size).limit(size).all()

        return friends, total

    def get_incoming_requests(self, user_id: int, page: int, size: int) -> tuple[list[Friend], int]:
        query = self.db_session.query(Friend).filter(
            Friend.friend_id == user_id,
            Friend.status_id == FriendStatusEnum.PENDING
        )
        total = query.count()
        incoming = query.order_by(Friend.created_at.desc()).offset((page - 1) * size).limit(size).all()

        return incoming, total

    def get_outgoing_requests(self, user_id: int, page: int, size: int) -> tuple[list[Friend], int]:
        query = self.db_session.query(Friend).filter(
            Friend.user_id == user_id,
            Friend.status_id == FriendStatusEnum.PENDING
        )
        total = query.count()
        outgoing = query.order_by(Friend.created_at.desc()).offset((page - 1) * size).limit(size).all()

        return outgoing, total

    def get_friendship(self, user_id: int, friend_id: int) -> Friend | None:
        friendship = self.db_session.query(Friend).filter(
            or_(
                (Friend.user_id == user_id) & (Friend.friend_id == friend_id),
                (Friend.user_id == friend_id) & (Friend.friend_id == user_id)
            )
        ).one_or_none()

        return friendship

    def create_friendship(self, user_id: int, friend_id: int) -> Friend:
        friend_request = Friend(
            user_id=user_id,
            friend_id=friend_id,
            status_id=FriendStatusEnum.PENDING
        )

        self.db_session.add(friend_request)
        self.db_session.commit()

        return friend_request

    def update_friendship_status(self, friendship: Friend, status: FriendStatusEnum) -> Friend:
        friendship.status_id = status
        self.db_session.commit()

        return friendship

    def delete_friendship(self, friendship: Friend) -> Friend:
        self.db_session.delete(friendship)
        self.db_session.commit()

        return friendship