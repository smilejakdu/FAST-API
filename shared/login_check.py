from requests import Request

import db
from models.user_entity import user_entity
from my_settings import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
import jwt
from starlette.responses import JSONResponse


async def login_check(access_token: str = None):
    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=ALGORITHM,
        )

        email = payload.get("sub")
        user = db.query(user_entity).filter(user_entity.email == email).first()
        if not user:
            return JSONResponse({
                "ok": False,
                "status_code": 401,
                "content": "INVALID_USER",
            })
        return user

    except jwt.DecodeError:
        return JSONResponse({
            "ok": False,
            "status_code": 401,
            "content": "INVALID_TOKEN",
        })
    except Exception as e:
        print(e)
        return JSONResponse({
            "ok": False,
            "status_code": 401
        })
