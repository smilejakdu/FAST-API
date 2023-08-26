import jwt
from fastapi import Request, Depends

from models.connection import get_db
from models.user_entity import user_entity
from my_settings import SECRET_KEY, ALGORITHM
from shared.error_response import CustomException


def login_check_service(func):
    async def wrapper(request: Request, user_repo, *args, **kwargs):
        try:
            get_access_token = request.cookies.get('access-token', None)
            payload = jwt.decode(get_access_token, SECRET_KEY, algorithms=ALGORITHM)
            user = await user_repo.find_user_by_email(payload['sub'])
            print('user:', user)

            # request.user에 user 정보를 저장
            request.state.user = user

            return await func(request, *args, **kwargs)
        except user_entity.DoesNotExist:
            raise CustomException(message="INVALID_USER", status_code=401)
        except jwt.DecodeError:
            raise CustomException(message="INVALID_TOKEN", status_code=400)
        except KeyError:
            raise CustomException(message="INVALID_KEY", status_code=400)
        except Exception as e:
            print(e)

    return wrapper
