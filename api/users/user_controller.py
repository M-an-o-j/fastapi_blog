from api.users.user_service import *
from utills.handlers import *
from api.users.user_service import *
from utills.auth_handler import *
from utills.validations import *

secret = SECRET_KEY

services = user_services()
user_validation = validations.User_validations()

class user_controller:
      def createUsercontroller(self,db, user):
            if user_validation.null_error_handler(user.name, user.username, user.password, user.email):
                  return errorhandler(400, "All field is required")
            if user_validation.empty_validation(user) == False:
                  return errorhandler(400, "All field is required")            
            if not user_validation.password_validation(user.password):
                  errorhandler(400,"Password should contain 8 character, atleast 1 uppercase letter, atleast 1 lowercase letter, atleast 1 symbol")            
            if not user_validation.email_validations(user.email):
                  errorhandler(400,"Email is not valid")
            return services.createuserservice(db, user)

      def loginusercontroller(self,db, user):
            if user_validation.null_validation(user.username, user.password):
                  return errorhandler(400,"All field is required")
            db_user = filter_items(db,User,User.username, user.username).first()
            if db_user:
                  if user_validation.User_delete_validation(db_user):
                        errorhandler(404, "User not found")
            if user_validation.empty_validation(user) == False:
                  errorhandler(400, "Username and password is required") 
            return services.loginUserservice(db, user)
      
      def logoutusercontroller(self,db,Auth_head):
            id = decode_token_id(Auth_head)
            db_user = filter_items(db,User,User.id,id).first()
            if not user_validation.login_validation(db_user):
                  errorhandler(401,"You can't logout unless loggedin")
            return services.logoutUserservice(db,id)
            
      def updateUsercontroller(self,db, user, Auth_head):
            id = decode_token_id(Auth_head)
            db_user = filter_items(db,User,User.id,id).first()            
            if user_validation.User_delete_validation(db_user):
                  errorhandler(404,"User not found")          
            if user.name == "" and user.username == "":
                  errorhandler(400, "Any one field is required")            
            return services.updateUserservice(db, user, id)
            
      def deleteUsercontroller(self,db, Auth_head):            
            id = decode_token_id(Auth_head)
            db_user = db.query(User).get(id)
            if not user_validation.login_validation(db_user):
                  errorhandler(401, "You have to login to delete your account")
            return services.deleteUserservice(db, id)
      
      def userProfilecontroller(self,db,Auth_head):      
            return services.userprofileservice(db, Auth_head)