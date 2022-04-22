from sqlalchemy import Column, Integer, String, Boolean
from db import Base


class UserEntity(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(200), nullable=False)
    nickname = Column(String(200), nullable=True)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
