from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    name:str
    username : str
    email : str 
    created_at: datetime

class UserSignUp(BaseModel):
    name:str
    username : str
    password : str
    email : str 

class Userlogin(BaseModel):
    username: str
    password: str

class loginresponse(BaseModel):
    username:str
    access_token: str
    token_type:str

class updateuserresponse(BaseModel):
    name:Optional[str]
    username:Optional[str]
