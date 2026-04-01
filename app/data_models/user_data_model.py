from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.enums.user_role_enum import UserRoleEnum
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    role_id = Column(Integer, ForeignKey("user_role.id"), nullable=False, default=UserRoleEnum.USER)

    messages_sent = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    messages_received = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    friends = relationship("Friend", foreign_keys="Friend.user_id", back_populates="user")
    posts = relationship("Post", foreign_keys="Post.user_id", back_populates="user")
    role = relationship("UserRole", foreign_keys=[role_id])
    liked_posts = relationship("PostLike", backref="user", cascade="all, delete-orphan")
    profile = relationship("Profile", uselist=False, back_populates="user", cascade="all, delete-orphan")
