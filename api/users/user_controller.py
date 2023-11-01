from fastapi import HTTPException, status
from api.users.user_service import *
from jose import jwt
import re
from configuration.config import *
from utills.error import error
from api.users.user_service import *

secret = SECRET_KEY

services = user_services()

class user_controller:
      def createUsercontroller(self,db, user):
            if user.name == "" or user.username == "" or user.password == "" or user.email == "":
                  error(400,"All field is required")
            
            PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
            if not PASSWORD_REGEX.match(user.password):
                  error(400,"Password should contain 8 character, atleast 1 uppercase letter, atleast 1 lowercase letter, atleast 1 symbol")
            
            EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$")
            if not EMAIL_REGEX.match(user.email):
                  error(400,"Email is not valid")

            return services.createuserservice(db, user)

      def loginusercontroller(self,db, user):

            db_user = db.query(User).filter(User.username == user.username).first()

            if db_user.is_deleted == True:
                  error(404, "User not found")
            if user.username == "" and user.password == "":
                  error(400, "Username and password is required")
            if user.username == "":
                  error(400, "Username is required")
            if user.password == "":
                  error(400, "password is required")
            
            return services.loginUserservice(db, user)
      
      def logoutusercontroller(self,db,user_id,token):
            try:
                  id = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
            except Exception as e:
                  error(401,"Invalid token")

            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user.is_active == False:
                  error(401,"you are not logged in ")

            if user_id != int(id):
                  error(401, "You can't delete this account")   

            return services.logoutUserservice(db,id)
            
      def updateUsercontroller(self,db, user,user_id, token):
            db_user = db.query(User).filter(User.id == user_id).first()

            try:
                  id = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
            except Exception as e:
                  error(401,"Invalid token")
            
            if db_user is None:
                  error(404,"User not found")           
            if user_id != int(id):
                  error(401, "You can't update this account")           
            if user.name == "" and user.username == "":
                  error(400, "Any one field is required")
            
            return services.updateUserservice(db, user, id)
            
      def deleteUsercontroller(self,db,token, user_id):
            try:
                  id = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
                  print("jwt id",id)
            except Exception as e:
                  error(401, "Invalid token")
            
            if user_id != int(id):
                  error(401, "You can't delete this account")
            
            return services.deleteUserservice(db, user_id)