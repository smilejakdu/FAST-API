from typing import Optional
from pydantic import BaseModel


class CoreResponse(BaseModel):
    ok: bool
    status_code: int
    message: str


class LoginResponse(CoreResponse):
    data: str
    access_token: Optional[str] = None


class MyInfoResponse(CoreResponse):
    data: str
