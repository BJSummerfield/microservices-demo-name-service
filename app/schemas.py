from pydantic import BaseModel 
from typing import Optional
import uuid

class NameBase(BaseModel):
    name: Optional[str] = None  

class NameCreate(NameBase):
    id: uuid.UUID  

class NameUpdate(BaseModel):
    name: Optional[str] = None

class Name(NameBase):
    id: uuid.UUID  

    class Config:
        from_attributes = True


