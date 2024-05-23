from pydantic import BaseModel
from typing import Optional
import uuid

class NameBase(BaseModel):
    name: str

class NameCreate(NameBase):
    id: Optional[uuid.UUID] = None

class Name(NameBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

