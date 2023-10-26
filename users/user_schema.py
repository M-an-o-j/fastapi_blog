from pydantic import BaseModel

class UserResponse(BaseModel):
    username : str
    password : str
    email : str 

class Userlogin(BaseModel):
    username: str
    password: str

class loginresponse(BaseModel):
    username:str
    password: str
    access_token: str
    token_type:str