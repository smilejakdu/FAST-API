from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from db import Base


class date_time_entity(Base):
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

