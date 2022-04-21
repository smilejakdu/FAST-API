from sqlalchemy.orm import Session
from models.TestEntity import TestEntity


def get_items(db: Session):
    return db.query(TestEntity).all()
