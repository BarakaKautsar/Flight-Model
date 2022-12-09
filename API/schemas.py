from pydantic import BaseModel

class User(BaseModel):
	username:str
	password:str
	email:str

class Plan(BaseModel):
    Quarter:int
    Origin: str
    Dest: str
    NumTicketsOrdered: int
    AirlineCompany: str

