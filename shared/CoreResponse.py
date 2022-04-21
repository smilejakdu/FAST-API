from typing import Optional

from pydantic import BaseModel


class CoreResponse(BaseModel):
    ok: bool
    status_code: int
    data: Optional[str] = None
    message: str
