from pydantic import BaseModel


class CoreResponse(BaseModel):
    ok: bool
    status_code: int
    message: str
