from http import HTTPStatus

import bcrypt
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import update
from sqlalchemy.orm import Session

from controller.dto.user_controller_dto.user_request_dto import UserDto
from models.connection import get_db
from models.user_entity import user_entity


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    async def create_user(self, body):
        new_user = user_entity()
        new_user.email = body.email
        new_user.nickname = body.nickname
        password_crypt = bcrypt.hashpw(body.password.encode('utf-8'),
                                       bcrypt.gensalt()).decode('utf-8')
        new_user.password = password_crypt
        new_user.is_active = True

        self.session.add(new_user)
        self.session.flush()
        self.session.commit()

        return {
            "ok": True,
            "status_code": 201,
            "message": "User created successfully"
        }

    def find_user_by_id(self, user_id: int):
        user = self.session.query(user_entity).filter(user_entity.id == user_id).first()
        return jsonable_encoder(user)

    def find_user_all(self):
        users = self.session.query(user_entity).all()
        return jsonable_encoder(users)

    async def find_user_by_email(self, user_email: str):
        user = self.session.query(user_entity).filter(user_entity.email == user_email).first()
        return jsonable_encoder(user)

    def update_user_by_id(self, user_id: int, body: UserDto):
        stmt = update(user_entity).where(user_entity.id == user_id).values(nickname=body.nickname). \
            execution_options(synchronize_session="fetch")
        self.session.execute(stmt)
        self.session.commit()
        return {
            "ok": True,
            "status_code": 200,
            "data": user_id,
            "message": "SUCCESS",
        }

    def update_user_by_email(self, user_id: int, body: UserDto):
        response_updated_user = update(user_entity).where(user_entity.id == user_id).values(nickname=body.nickname). \
            execution_options(synchronize_session="fetch")
        self.session.execute(response_updated_user)
        self.session.commit()
        return {
            "ok": True,
            "status_code": HTTPStatus.OK,
            "data": user_id,
            "message": "SUCCESS",
        }
