from sqlalchemy import Column, String, Integer
from models.session import Base


class TestEntity(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)