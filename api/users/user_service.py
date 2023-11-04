from utills.auth_handler import *
from fastapi.responses import JSONResponse
from api.users.user_model import *
import datetime
from utills.handlers import *

expiry_del = ACCESS_TOKEN_EXPIRY_MINUTES

class user_services:
    def createuserservice(self,db, user):
            try:
                hashed_passowrd = hash_password(user.password)
                user.password = hashed_passowrd
                db_users = User(**user.dict(), created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                print(db_users)
                db.add(db_users)
                db.commit()
                db.refresh(db_users)
                return JSONResponse({
                    "message":f"Signed Up successfully",
                    "Greetings":f"Welcome {db_users.username}",
                    "user":{
                        "name":db_users.name,
                        "username":db_users.username,
                        "email":db_users.email
                    }
                })
            except Exception as e:
               errorhandler(500, "Internal server error")

    def loginUserservice(self,db, user):
            try:
                db_user = authenticate_user(db,user.username, user.password)
                db_user.is_active = True
                signin_log = Signin_logs(user_id= db_user.id, logged_in = datetime.datetime.now())
                access_token = create_access_token(data={"sub": str(db_user.id)}, expires_delta=expiry_del)
                db_token = Token(user_id= db_user.id, token=access_token)
                db.add(db_user)
                db.add(signin_log)
                db.add(db_token)
                db.commit()           
                return JSONResponse({
                    "message":"User loggedin successfully",
                    "user":{
                        "username":user.username,
                        "access_token": access_token, 
                        "token_type": "bearer"}
                    })
            except Exception as e:
               errorhandler(500, "Internal server error")
    
    def logoutUserservice(self,db, User_id):
          try:
                db_user = db.query(User).filter(User.id == User_id).first()
                db_user.is_active = False
                signin_user = filter_items(db,Signin_logs,Signin_logs.user_id,User_id).all()
                list_signin = [i.id for i in signin_user]
                last_login_id = max(list_signin)
                last_login = filter_items(db,Signin_logs, Signin_logs.id,last_login_id).first()
                last_login.logged_out = datetime.datetime.now()
                db_token = filter_items(db,Token,Token.user_id,User_id).first()
                db.add(last_login)
                db.delete(db_token)
                db.commit()
                return JSONResponse({
                        "message":"logged out"
                })
          except Exception as e:
               errorhandler(500, "Internal server error")

    def updateUserservice(self,db,user, username):
            try:
                db_user = db.query(User).filter(User.id == username).first()
                if user.username != "" and user.username != None:
                    db_user.username = user.username
                if user.name != "" and user.name != None:   
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
            except Exception as e:
                errorhandler(500, "Internal server error")

    def deleteUserservice(self,db, user_id):
        try:
            db_token = filter_items(db,Token,Token.user_id,user_id).first()
            db_user = db.query(User).get(user_id)
            db_user.is_deleted = True
            db.delete(db_token)
            db.commit()
            return JSONResponse({
                    "message": "account deleted succesfully"
            })
        except Exception as e:
            errorhandler(500, "Internal server error")
    
    def userprofileservice(self, db, db_user):
          try:
            return db_user
          except Exception as e:
            errorhandler(500, "Internal server error")
          
    