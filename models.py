from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., example="johndoe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    full_name: Optional[str] = Field(None, example="John Doe")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="secret123")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, example="john.new@example.com")
    full_name: Optional[str] = Field(None, example="John New")
    password: Optional[str] = Field(None, min_length=6, example="newpass123")

class User(UserBase):
    id: int