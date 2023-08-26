from typing import Optional

import jwt
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models.user_entity import user_entity
from my_settings import SECRET_KEY, ALGORITHM
from repository.user_repository import UserRepository


async def login_check(
    user_repo: UserRepository,
    access_token: str = None
) -> Optional[user_entity]:
    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=ALGORITHM,
        )

        email = payload.get("sub")
        print("login_check email:", email)
        user = await user_repo.find_user_by_email(user_email=email)

        if not user:
            raise HTTPException(status_code=401, detail="Item not found")
        user_dict = jsonable_encoder(user)
        return user_dict

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token Decode Error")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token Decode Error")
