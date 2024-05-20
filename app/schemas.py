from pydantic import BaseModel
from typing import Optional
import uuid

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    id: Optional[uuid.UUID] = None

class User(UserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

