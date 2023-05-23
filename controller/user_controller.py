from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from controller.dto.UserControllerDto.UserRequestDto import createRequestDto, updateRequestDto, loginRequestDto
from models.connection import get_db
from services import user_service
from shared.core_response import CoreResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/find_user_all", status_code=200)
def find_user(db: Session = Depends(get_db)):
    return user_service.find_user_all(db)


@router.post("/sign_up", response_model=CoreResponse, status_code=201)
def create_user(body: createRequestDto, db: Session = Depends(get_db)):
    return user_service.create_user(body, db)


@router.post("/login", response_model=CoreResponse, status_code=200)
async def login_user(body: loginRequestDto):
    return user_service.login_user(body)


@router.get("/{user_id}", status_code=200)
async def find_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.find_user_by_id(db, user_id)


@router.put("/{user_id}", response_model=CoreResponse, status_code=200)
async def update_user(body: updateRequestDto, user_id: int):
    return user_service.update_user(user_id, body)
