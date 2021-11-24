from typing import Optional, List
from pydantic import BaseModel

class SessionData(BaseModel):
    full_name: Optional[str]
    token: Optional[str]
    email: Optional[str]
