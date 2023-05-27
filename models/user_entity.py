from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from db import Base
from models.board_entity import board_entity


class user_entity(Base):
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(200), nullable=False)
    nickname = Column(String(200), nullable=True)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    boards = relationship("board_entity", back_populates="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
