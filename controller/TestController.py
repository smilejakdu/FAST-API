# routes/test.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.connection import get_db
from services import TestService

router = APIRouter(
    prefix="/test",  # url 앞에 고정적으로 붙는 경로추가
    tags=["test"],
)  # Route 분리


@router.get("/test_route")  # Route Path
def test_index(db: Session = Depends(get_db)):
    res = TestService.test_index(db=db)  # apis 호출

    return {
        "res": res,
    }  # 결과