from sqlalchemy import Enum


class UserRoleEnum(Enum):
    MODERATOR = 1
    USER = 2
