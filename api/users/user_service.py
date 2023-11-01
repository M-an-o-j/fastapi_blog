from utills.auth_handler import *
from fastapi.responses import JSONResponse
from api.users.user_model import *
import datetime

expiry_del = ACCESS_TOKEN_EXPIRY_MINUTES

class user_services:
    def createuserservice(self,db, user):
            hashed_passowrd = hash_password(user.password)
            user.password = hashed_passowrd
            db_users = User(**user.dict(), created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(db_users)
            db.add(db_users)
            db.commit()
            db.refresh(db_users)
            return JSONResponse({
                "message":f"Signed Up successfully",
                "Greetings":f"Welcome {db_users.username}"
            })

    def loginUserservice(self,db, user):
            db_user = authenticate_user(db,user.username, user.password)
            db_user.is_active = True
            signin_log = Signin_logs(user_id= db_user.id, logged_in = datetime.datetime.now())
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
    def logoutUserservice(self,db, User_id):
          db_user = db.query(User).filter(User.id == User_id).first()
          db_user.is_active = False
          signin_user = db.query(Signin_logs).filter(Signin_logs.user_id == User_id).all()
          signin_user_ids = [i.id for i in signin_user]
          last_login_id = max(signin_user_ids)
          last_login = db.query(Signin_logs).filter(Signin_logs.id == last_login_id).first()
          last_login.logged_out = datetime.datetime.now()
          db.add(last_login)
          db.commit()
          return JSONResponse({
                "message":"logged out"
          })

    def updateUserservice(self,db,user, username):
            print(username)
            db_user = db.query(User).filter(User.id == username).first()
            print(db_user.created_at)
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

    def deleteUserservice(self,db, user_id):
        db_user = db.query(User).get(user_id)
        db_user.is_deleted = True
        db.commit()

        return JSONResponse({
                "message": "account deleted succesfully"
        })
    
    def userprofileservice(self, db, user_id):
          db_user = db.query(User).get(user_id)

          return db_user
          
    