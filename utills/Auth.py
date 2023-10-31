from passlib.hash import bcrypt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union
from api.users.user_model import *
from jose import jwt
from fastapi import HTTPException
from configuration.config import SECRET_KEY


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