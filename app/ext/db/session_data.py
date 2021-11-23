from typing import Optional, List
from pydantic import BaseModel
#from sqlmodel import Field, SQLModel

class SessionData(BaseModel):
    full_name: str
    token: str
    email: str
