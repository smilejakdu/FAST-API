from fastapi import APIRouter , Depends
from typing import List
from starlette.middleware.cors import CORSMiddleware

from db import session
from models import UserTable, User

app = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

@app.get("")
def read_users():
    users = session.query(UserTable).all()
    return read_users


@app.get("/{user_id}")
def read_user(user_id: int):
    user = session.query(UserTable).filter(UserTable.id == user_id).first()
    return user


@app.post("")
def create_users(name: str, age: int):
    user = UserTable()
    user.name = name
    user.age = age

    session.add(user)
    session.commit()
    return f"{name} created..."


@app.put("")
def update_users(users: List[User]):
    for i in users:
        user = session.query(UserTable).filter(UserTable.id == i.id).first()
        user.name = i.name
        user.age = i.age
    return f"{users[0].name} updated..."


@app.delete("")
def delete_user(user_id: int):
    user = session.query(UserTable).filter(UserTable.id == user_id).delete()
    session.commit()
    return user
