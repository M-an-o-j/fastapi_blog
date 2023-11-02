from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    name:str
    username : str
    email : str 
    created_at: datetime

class UserSignUp(BaseModel):
    name:str = None
    username : str = None
    password : str = None
    email : str = None

class Userlogin(BaseModel):
    username: str = None
    password: str = None

class loginresponse(BaseModel):
    username:str
    access_token: str
    token_type:str

class updateuserresponse(BaseModel):
    name:str = None
    username:str = None
