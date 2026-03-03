from sqlalchemy import Column, Integer, String
from database import Base

class FriendStatus(Base):
    __tablename__ = "friend_status"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False, unique=True)
