from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db import Base
from models.UserEntity import UserEntity


class BoardEntity(Base):
    __tablename__ = 'boards'
    id: Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(UserEntity, back_populates="boards")
