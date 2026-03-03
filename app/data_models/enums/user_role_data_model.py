from database import Base
from sqlalchemy import Integer, String, Column

class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False, unique=True)
