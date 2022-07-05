from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class SeeUser(BaseModel):
    email: EmailStr
    created_at: datetime
    name: str

    class Config:           #pydantic работает только с dict, эта строчка позволяет работать с любым типом
        orm_mode = True

class PostUser(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: SeeUser

    class Config:           #pydantic работает только с dict, эта строчка позволяет работать с любым типом
        orm_mode = True


class RespUser(BaseModel):
    id: str
    created_at: datetime

    class Config:           #pydantic работает только с dict, эта строчка позволяет работать с любым типом
        orm_mode = True


class NewUser(BaseModel):
    email: EmailStr
    password: str
    name: str


    class Config:           #pydantic работает только с dict, эта строчка позволяет работать с любым типом
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class PostWithVotes(BaseModel):
    Post: PostUser
    votes: int


