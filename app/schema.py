from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

class User(BaseModel):

    id: int | None
    email: EmailStr
    password: str

class UserResponse(BaseModel):

    id: int
    email: EmailStr

class Post(BaseModel):

    id: int | None
    title: str
    content: str
    #published: Optional[bool] = True

class PostResponse(BaseModel):

    title: str
    content: str
    created_at: datetime
    votes: int
    email: EmailStr

class UserLogin(BaseModel):

    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str | None = "bearer"

class TokenData(BaseModel):

    id: str

class Vote(BaseModel):

    post_id: int
    dir: conint(le=1)