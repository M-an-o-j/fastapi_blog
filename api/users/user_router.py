from api.users.user_schema import *
from sqlalchemy.orm import Session
from api.users.user_controller import *
from utills.auth_bearer import * 

controller =  user_controller()

httpbearer = AdminJWT()

@router.post("/signup", response_model=UserResponse, summary="Create an user",description="User can signup in this endpoint ", tags=["User"])
async def signup(user: UserSignUp , db: Session = Depends(get_session) ):
    return controller.createUsercontroller(db, user)

@router.post("/signin", response_model=loginresponse, summary="Login User", description="User can login in this endpoint", tags=["User"])
async def signin(user: Userlogin, db:Session = Depends(get_session)):
    return controller.loginusercontroller(db, user)

@router.put("/update/", response_model=updateuserresponse,dependencies = [Depends(httpbearer)], summary="Update User", description="User can update their details in this endpoint", tags=["User"] )
async def updateuser(user: updateuserresponse,Auth_head:str = Depends(get_authorization_header), db:Session = Depends(get_session)):
    return controller.updateUsercontroller(db, user,Auth_head)

@router.delete("/delete/", response_model=updateuserresponse,dependencies = [Depends(httpbearer)], summary="Delete User", description="User can delete their account in this endpoint", tags=["User"] )
async def updateuser(Auth_head:str = Depends(get_authorization_header),db:Session = Depends(get_session)):
    return controller.deleteUsercontroller(db, Auth_head)

@router.post("/logout/", response_model=updateuserresponse,dependencies = [Depends(httpbearer)], summary="logout User", description="User can logout in this endpoint", tags=["User"] )
async def updateuser(Auth_head:str = Depends(get_authorization_header),db:Session = Depends(get_session)):
    return controller.logoutusercontroller(db,Auth_head)

@router.get("/my_profile/", response_model=UserResponse,dependencies = [Depends(httpbearer)] ,summary="user profile", description="user can see their own profile here", tags=["User"] )
async def updateuser( Auth_head:str = Depends(get_authorization_header),db:Session = Depends(get_session)):
    return controller.userProfilecontroller(db, Auth_head)


