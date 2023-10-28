from models import User
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from Auth import hash_password, verify_password, authenticate_user, create_access_token
from api.users.user_service import createuserservice, loginUserservice, updateUserservice
from config import ACCESS_TOKEN_EXPIRY_MINUTES
from jose import jwt

from config import SECRET_KEY
import re

secret = SECRET_KEY

expiry_del = ACCESS_TOKEN_EXPIRY_MINUTES

def createUsercontroller(db, user):
        if user.name == "" or user.username == "" or user.password == "" or user.email == "":
              raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All field is required")
        
        PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
        if not PASSWORD_REGEX.match(user.password):
              raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password should contain 8 character, atleast 1 uppercase letter, atleast 1 lowercase letter, atleast 1 symbol")
        
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$")
        if not EMAIL_REGEX.match(user.email):
              raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email is not valid")
        return createuserservice(db, user)

def loginusercontroller(db, user):
        if user.username == "" and user.password == "":
              raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and password is required")
        if user.username == "":
              raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is required")
        if user.password == "":
              raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password is required")
        
        return loginUserservice(db, user)
        

def updateUsercontroller(db, user, token):
        
        try:
            username = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        
        if user.name == "" and user.username == "":
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Any one field is required") 
        return updateUserservice(db, user, username)
        

