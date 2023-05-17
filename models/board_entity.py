from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from models import user_entity
from db import Base


class board_entity(Base):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(user_entity, back_populates="boards")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
