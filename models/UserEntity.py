from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db import Base
from models.BoardEntity import BoardEntity


class UserEntity(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(200), nullable=False)
    nickname = Column(String(200), nullable=True)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    board = relationship(BoardEntity, back_populates="users")
