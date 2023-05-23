from sqlalchemy.orm import Session
from models.test_entity import TestEntity


def get_items(db: Session):
    return db.query(TestEntity).all()
