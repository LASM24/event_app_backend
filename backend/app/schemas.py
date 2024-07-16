from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class LoginUser(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class EventBase(BaseModel):
    title: str
    description: str
    date: datetime
    image: str
    max_capacity: int

class EventCreate(EventBase):
    owner_id: int

class EventOut(BaseModel):
    id: int
    title: str
    description: str
    date: datetime
    image: str
    owner_username: str
    owner_id: int  # Puedes marcar estos como opcionales
    max_capacity: int

    class Config:
        orm_mode = True

class Event(EventBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class RegistrationBase(BaseModel):
    event_id: int
    user_id: int

class RegistrationCreate(RegistrationBase):
    pass

class Registration(RegistrationBase):
    id: int

    class Config:
        orm_mode = True

class RegistrationWithUser(Registration):
    user: User
