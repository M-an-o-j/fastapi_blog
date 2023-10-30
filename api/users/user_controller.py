from models import User
from fastapi import HTTPException, status
from api.users.user_service import user_services
from config import ACCESS_TOKEN_EXPIRY_MINUTES
from jose import jwt

from config import SECRET_KEY
import re

secret = SECRET_KEY

expiry_del = ACCESS_TOKEN_EXPIRY_MINUTES

class user_controller:
      def createUsercontroller(self,db, user):
            if user.name == "" or user.username == "" or user.password == "" or user.email == "":
                  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All field is required")
            
            PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
            if not PASSWORD_REGEX.match(user.password):
                  raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password should contain 8 character, atleast 1 uppercase letter, atleast 1 lowercase letter, atleast 1 symbol")
            
            EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$")
            if not EMAIL_REGEX.match(user.email):
                  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email is not valid")
            return user_services.createuserservice(db, user)

      def loginusercontroller(self,db, user):
            if user.username == "" and user.password == "":
                  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and password is required")
            if user.username == "":
                  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is required")
            if user.password == "":
                  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password is required")
            
            return user_services.loginUserservice(db, user)
            
      def updateUsercontroller(self,db, user,user_id, token):
            try:
                  id = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
            except Exception as e:
                  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
            
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user is None:
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
            if user_id != id:
                  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't update this account")
            
            if user.name == "" and user.username == "":
                  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Any one field is required") 
            
            return user_services.updateUserservice(db, user, id)
            
      def deleteUsercontroller(self,db,token, user_id):
            try:
                  id = jwt.decode(token, secret, algorithms=["HS256"])["sub"]
            except Exception as e:
                  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
            
            if user_id != id:
                  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't delete this account")
            
            return user_services.deleteUserservice(db, user_id)