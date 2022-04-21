from sqlalchemy.orm import Session
from models.UserEntity import UserEntity

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def create_user(db: Session, body):
    user = UserEntity()
    user.email = body.email
    user.password = body.password
    user.is_active = True

    db.add(user)

    db.commit()

    return {
        "status_code": 201,
    }


def find_user_by_id(db: Session, user_id: int):
    user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
    return jsonable_encoder(user)


def find_user_by_email(db: Session, user_email: str):
    user = db.query(UserEntity).filter(UserEntity.email == user_email).first()
    print('user:', jsonable_encoder(user))
    return jsonable_encoder(user)


def update_user_by_id(db: Session, user_id: int):
    user = find_user_by_id(user_id)
    user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
    return JSONResponse(content=jsonable_encoder(user))
