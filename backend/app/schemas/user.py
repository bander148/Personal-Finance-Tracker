from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, validator, Field, field_validator


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: EmailStr
    id : int
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str


