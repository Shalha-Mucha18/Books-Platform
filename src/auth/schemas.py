from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional,List
import uuid
from datetime import datetime
from src.books.schemas import BookCreate


class UserCreateModel(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str 
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str


class UserModel(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
    book: List[BookCreate] 


class UserLoginModel(BaseModel):
    email: str
    password: str
  
