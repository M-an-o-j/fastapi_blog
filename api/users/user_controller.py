from api.users.user_service import *
from utills.handlers import *
from api.users.user_service import *
from utills.auth_handler import *
from utills.validations import *
from .user_schema import *

secret = SECRET_KEY

class user_controller(Validations, user_services):
      def createUsercontroller(self,db, user):
            try:
                  # Validate the missing field
                  if super().None_validation(user.name, user.username, user.password, user.email):
                        return errorhandler(400, "All field is required")
                  # Validate the empty field
                  if super().empty_validation(user) == False:
                        return errorhandler(400, "Fields shoudn't be empty") 
                  # Validate the password format          
                  if not super().password_validation(user.password):
                        errorhandler(400,"Password should contain 8 character, atleast 1 uppercase letter, atleast 1 lowercase letter, atleast 1 symbol")            
                  # Validate the email format      
                  if not super().email_validations(user.email):
                        errorhandler(400,"Email is not valid")
                  # returning the create user service function
                  return super().createuserservice(db, user)
            except ValidationError as e:
                  for error in e.errors():
                        errorhandler(422,f"{error['msg']}")

      def loginusercontroller(self,db, user):
            # Validate the missing field
            if super().None_validation(user.username, user.password):
                  return errorhandler(400,"All field is required")
            # Getting the user object using filter_item function
            db_user = filter_items(db,User,User.username, user.username).first()
            print(db_user.name)
            # if user object exist
            if db_user:
                  # Validate the user is deleted or not
                  if super().User_delete_validation(db_user):
                        errorhandler(404, "User not found")
            # validate the empty field
            if super().empty_validation(user) == False:
                  errorhandler(400, "Username and password is required") 
            # Returning the user login service
            return super().loginUserservice(db, user)
      
      def logoutusercontroller(self,db,Auth_head):
            # Taking apart the id from the token 
            id = decode_token_id(Auth_head,db)
            # Fetching the user object using filter_item function
            db_user = filter_items(db,User,User.id,id).first()
            # Validate the user is deleted or not
            if super().User_delete_validation(db_user):
                  errorhandler(404,"User not found") 
            # Validate the user is logged in or not
            if not super().login_validation(db_user):
                  errorhandler(401,"You can't logout unless loggedin")
            # Returning the logout User service
            return super().logoutUserservice(db,id)
            
      def updateUsercontroller(self,db, user, Auth_head):
            # Taking apart the id from the token
            id = decode_token_id(Auth_head,db)
            # Fetching the user object using filter_item function
            db_user = filter_items(db,User,User.id,id).first()
            # Validate the user is deleted or not            
            if super().User_delete_validation(db_user):
                  errorhandler(404,"User not found") 
            # Validate that both field's are empty or not         
            if user.name == "" and user.username == "":
                  errorhandler(400, "Any one field is required")
            # Returning the User update service            
            return super().updateUserservice(db, user, id)
            
      def deleteUsercontroller(self,db, Auth_head):
            # Taking apart the id from the token            
            id = decode_token_id(Auth_head,db)
            # Fetching the user object using filter_item function
            db_user = filter_items(db,User,User.id,id).first()
            # Validate the user is deleted or not  
            if not super().login_validation(db_user):
                  errorhandler(401, "You have to login to delete your account")
            # Returning the delete user service
            return super().deleteUserservice(db, id)
      
      def userProfilecontroller(self,db,Auth_head):
            id = decode_token_id(Auth_head,db)
            # Fetching the user object using filter_item function
            db_user = filter_items(db,User,User.id,id).first()
            # Validate the user is deleted or not  
            if super().User_delete_validation(db_user):
                  errorhandler(404,"User not found")   
            # Returning the user profile service   
            return super().userprofileservice(db, db_user)