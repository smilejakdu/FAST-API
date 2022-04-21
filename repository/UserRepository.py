from sqlalchemy.orm import Session
from models.UserEntity import UserEntity

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def create_users(db: Session, name: str, age: int):
    user = UserEntity()
    user.name = name
    user.age = age

    db.add(user)
    db.commit()

    return {
        "status_code": 200,
    }


def get_user_by_id(db: Session, user_id: int):
    user = db.query(UserEntity)
    if user_id:
        user.filter(UserEntity.id == user_id).first()
    json_compatible_item_data = jsonable_encoder(user)
    return JSONResponse(content=json_compatible_item_data)
