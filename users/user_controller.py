from models import User
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from Auth import hash_password, verify_password, authenticate_user, create_access_token
from config import ACCESS_TOKEN_EXPIRY_MINUTES

expiry_del = ACCESS_TOKEN_EXPIRY_MINUTES

def createUser(db, user):
    try:
        hashed_passowrd = hash_password(user.password)
        user.password = hashed_passowrd
        db_users = User(**user.dict())
        db.add(db_users)
        db.commit()
        db.refresh(db_users)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "message": f"error:{e}"
        })
    return JSONResponse({
         "message":f"Signed Up successfully",
         "Greetings":f"Welcome {db_users.username}"
    })

def loginuser(db, user):
        db_user = authenticate_user(db,user.username, user.password)
        db_user.active = True
        db.add(db_user)
        db.commit()
        access_token = create_access_token(data={"sub": user.username}, expires_delta=expiry_del)
        return JSONResponse({
             "message":"User loggedin successfully",
             "user":{
                "username":user.username, 
                "password": user.password,
                "access_token": access_token, 
                "token_type": "bearer"}
             })
