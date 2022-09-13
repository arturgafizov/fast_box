from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class UserBase(BaseModel):
    email: str
    role: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
