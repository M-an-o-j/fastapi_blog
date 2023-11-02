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
            # Validate the missing field
            if user_validation.None_validation(user.name, user.username, user.password, user.email):
                  return errorhandler(400, "All field is required")
            # Validate the empty field
            if user_validation.empty_validation(user) == False:
                  return errorhandler(400, "All field is required") 
            # Validate the password format          
            if not user_validation.password_validation(user.password):
                  errorhandler(400,"Password should contain 8 character, atleast 1 uppercase letter, atleast 1 lowercase letter, atleast 1 symbol")            
            # Validate the email format      
            if not user_validation.email_validations(user.email):
                  errorhandler(400,"Email is not valid")
            # returning the create user service function
            return services.createuserservice(db, user)

      def loginusercontroller(self,db, user):
            # Validate the missing field
            if user_validation.None_validation(user.username, user.password):
                  return errorhandler(400,"All field is required")
            # Getting the user object using filter_item function
            db_user = filter_items(db,User,User.username, user.username).first()
            # if user object exist
            if db_user:
                  # Validate the user is deleted or not
                  if user_validation.User_delete_validation(db_user):
                        errorhandler(404, "User not found")
            # validate the empty field
            if user_validation.empty_validation(user) == False:
                  errorhandler(400, "Username and password is required") 
            # Returning the user login service
            return services.loginUserservice(db, user)
      
      def logoutusercontroller(self,db,Auth_head):
            # Taking apart the id from the token 
            id = decode_token_id(Auth_head,db)
            # Fetching the user object using filter_item function
            db_user = filter_items(db,User,User.id,id).first()
            # Validate the user is deleted or not
            if user_validation.User_delete_validation(db_user):
                  errorhandler(404,"User not found") 
            # Validate the user is logged in or not
            if not user_validation.login_validation(db_user):
                  errorhandler(401,"You can't logout unless loggedin")
            # Returning the logout User service
            return services.logoutUserservice(db,id)
            
      def updateUsercontroller(self,db, user, Auth_head):
            # Taking apart the id from the token
            id = decode_token_id(Auth_head,db)
            # Fetching the user object using filter_item function
            db_user = filter_items(db,User,User.id,id).first()
            # Validate the user is deleted or not            
            if user_validation.User_delete_validation(db_user):
                  errorhandler(404,"User not found") 
            # Validate that both field's are empty or not         
            if user.name == "" and user.username == "":
                  errorhandler(400, "Any one field is required")
            # Returning the User update service            
            return services.updateUserservice(db, user, id)
            
      def deleteUsercontroller(self,db, Auth_head):
            # Taking apart the id from the token            
            id = decode_token_id(Auth_head,db)
            # Fetching the user object using filter_item function
            db_user = filter_items(db,User,User.id == id).first()
            # Validate the user is deleted or not  
            if not user_validation.login_validation(db_user):
                  errorhandler(401, "You have to login to delete your account")
            # Returning the delete user service
            return services.deleteUserservice(db, id)
      
      def userProfilecontroller(self,db,Auth_head):
            id = decode_token_id(Auth_head,db)
            # Fetching the user object using filter_item function
            db_user = filter_items(db,User,User.id == id).first()
            # Validate the user is deleted or not  
            if user_validation.User_delete_validation(db_user):
                  errorhandler(404,"User not found")   
            # Returning the user profile service   
            return services.userprofileservice(db, db_user)