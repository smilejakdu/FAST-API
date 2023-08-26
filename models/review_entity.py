from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship

from db import Base


class review_entity(Base):
    __tablename__ = 'reviews'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(200), nullable=True)
    board_id = Column(Integer, ForeignKey('boards.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    board = relationship("board_entity", back_populates="reviews")
    user = relationship("user_entity", back_populates="reviews")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    @classmethod
    def create(cls, content: str, board_id: int, user_id: int) -> "review_entity":
        return cls(
            content=content,
            board_id=board_id,
            user_id=user_id
        )
