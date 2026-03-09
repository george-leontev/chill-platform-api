from enum import Enum


class FriendStatusEnum(int, Enum):
    PENDING = 1
    ACCEPTED = 2
    DECLINED = 3
