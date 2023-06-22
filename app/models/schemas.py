from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    company: Optional[str]


class UserPayload(BaseUser):
    password: str

    class Config:
        orm_mode = True


class UserResponse(BaseUser):
    id: int

    class Config:
        orm_mode = True


class BaseLead(BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str


class LeadPayload(BaseLead):
    pass


class LeadResponse(BaseLead):
    id: int
    owner_id: int
    date_created: datetime
    date_updated: datetime

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
