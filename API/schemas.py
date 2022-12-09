from pydantic import BaseModel, Field, EmailStr
import datetime as _dt

class _UserBase(BaseModel):
    email: str

class UserCreate(_UserBase):
    password: str

    class Config:
        orm_mode = True

class User(_UserBase):
    id: int
    date_created: _dt.datetime

    class Config:
        orm_mode = True


class Plan(BaseModel):
    Quarter:int
    Origin: str
    Dest: str
    NumTicketsOrdered: int
    AirlineCompany: str

