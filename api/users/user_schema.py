from pydantic import BaseModel

class UserResponse(BaseModel):
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
    name:str
    username:str
