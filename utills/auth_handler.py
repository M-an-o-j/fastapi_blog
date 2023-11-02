from passlib.hash import bcrypt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union
from api.users.user_model import *
from jose import jwt
from fastapi import HTTPException, Request
import time

ACCESS_TOKEN_EXPIRY_MINUTES = 30
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str, db):
    user_det = db.query(User).filter(User.username == username).first()
    if user_det is not None:
        return user_det
    raise HTTPException(status_code=404, detail="User not found")

def authenticate_user(db, username: str, password: str):
    user = get_user(username, db)
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def decode_token(token):
    decode_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    expires = decode_token.get("exp")
    if expires >= time.time():
        return str(decode_token)
    
def decode_token_id(token):
    print(token)
    decode_token = jwt.decode(token.split("Bearer")[1].strip(), SECRET_KEY, algorithms=["HS256"])['sub']
    return int(decode_token)
    
def get_authorization_header(request: Request):
    return request.headers.get("Authorization")