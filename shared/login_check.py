from typing import Type, Optional

import jwt
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models.user_entity import user_entity
from my_settings import SECRET_KEY, ALGORITHM


async def login_check(
    db: Session,
    access_token: str = None
) -> Optional[user_entity]:
    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=ALGORITHM,
        )

        email = payload.get("sub")
        user = db.query(user_entity).filter(user_entity.email == email).first()

        if not user:
            raise HTTPException(status_code=401, detail="Item not found")
        user_dict = jsonable_encoder(user)
        return user_dict

    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token Decode Error")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token Decode Error")
