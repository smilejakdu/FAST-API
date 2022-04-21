from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from db import Base


class UserEntity(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)

