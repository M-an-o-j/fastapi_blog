from passlib.hash import bcrypt
from passlib.context import CryptContext
from users.user_model import User
from datetime import datetime, timedelta
from typing import Union
from config import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_user(username: str, db):
    print(username == "karthi")
    user_det = db.query(User).filter(User.username == username).first()
    users = db.query(User).all()
    print(user_det)
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return user_det

def authenticate_user(db, username: str, password: str):
    print("1")
    user = get_user(username, db)
    print(2)
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt