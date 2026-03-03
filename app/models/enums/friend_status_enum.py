from sqlalchemy import Enum


class FriendStatusEnum(Enum):
    PENDING = 1
    ACCEPTED = 2
