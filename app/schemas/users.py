from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Annotated

class UserBase(BaseModel):
    username: str
    fullname: str | None = None

class CreateUser(UserBase):
    email: EmailStr
    password: Annotated[str, Field(min_length=8, description= "password must be more than 8 character")]

class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8, description= "password must be more than 8 character")]

class ResponseUser(BaseModel):
    userid: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UpdateUser(CreateUser):
    pass
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None