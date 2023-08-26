from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime

from db import Base


class board_entity(Base):
    __tablename__ = 'boards'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("user_entity", back_populates="boards")
    reviews = relationship("review_entity", back_populates="board")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    @classmethod
    def create(cls, title: str, content: str, user_id: int) -> "board_entity":
        return cls(
            title=title,
            content=content,
            user_id=user_id
        )

    def delete(self) -> "board_entity":
        self.deleted_at = datetime.now()
        return self
