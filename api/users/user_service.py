from Auth import hash_password, verify_password, authenticate_user, create_access_token
from models import User
from fastapi.responses import JSONResponse
from config import ACCESS_TOKEN_EXPIRY_MINUTES, SECRET_KEY
from jose import jwt
import json
from api.users.user_model import Signin_logs
import datetime

expiry_del = ACCESS_TOKEN_EXPIRY_MINUTES

secret = SECRET_KEY

def createuserservice(db, user):
        hashed_passowrd = hash_password(user.password)
        user.password = hashed_passowrd
        db_users = User(**user.dict(), created_at = datetime.datetime.now())
        print(db_users)
        db.add(db_users)
        db.commit()
        db.refresh(db_users)
        return JSONResponse({
            "message":f"Signed Up successfully",
            "Greetings":f"Welcome {db_users.username}"
        })

def loginUserservice(db, user):
        db_user = authenticate_user(db,user.username, user.password)
        db_user.active = True
        signin_log = Signin_logs(user_id= db_user.id, Date_Time = datetime.datetime.now())
        print(signin_log)
        db.add(db_user)
        db.add(signin_log)
        db.commit()
        
        access_token = create_access_token(data={"sub": str(db_user.id)}, expires_delta=expiry_del)
        return JSONResponse({
             "message":"User loggedin successfully",
             "user":{
                "username":user.username,
                "access_token": access_token, 
                "token_type": "bearer"}
             })

def updateUserservice(db,user, username):
        # username = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
        print(username)
        db_user = db.query(User).filter(User.id == username).first()
        print(db_user.username)
        if user.username is not None:
            db_user.username = user.username
        if user.name is not None:   
            db_user.name = user.name
        print(db_user.username)

        db_user.updated_at = datetime.datetime.now()
        db.commit()
        return JSONResponse({
            "user":{
                 "name":db_user.name,
                 "username":db_user.username
            }
        })

def deleteUserservice(db, user_id):
      db_user = db.query(User).filter(User.id == user_id).first()
      db.delete(db_user)
      db.commit()

      return JSONResponse({
            "message":"account deleted succesfully"
      })