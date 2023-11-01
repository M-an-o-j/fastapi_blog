from api.users.user_schema import *
from sqlalchemy.orm import Session
from api.users.user_controller import *

controller =  user_controller()

@router.post("/signup", response_model=UserResponse, summary="Create an user",description="User can signup in this endpoint ", tags=["User"])
async def signup(user: UserSignUp , db: Session = Depends(get_session) ):
    return controller.createUsercontroller(db, user)

@router.post("/signin", response_model=loginresponse, summary="Login User", description="User can login in this endpoint", tags=["User"])
async def signin(user: Userlogin, db:Session = Depends(get_session)):
    return controller.loginusercontroller(db, user)

@router.put("/update/{user_id}", response_model=updateuserresponse, summary="Update User", description="User can update their details in this endpoint", tags=["User"] )
async def updateuser(user_id:int,user: updateuserresponse, db:Session = Depends(get_session), token=str):
    return controller.updateUsercontroller(db, user,user_id, token)

@router.delete("/delete/{user_id}", response_model=updateuserresponse, summary="Delete User", description="User can delete their account in this endpoint", tags=["User"] )
async def updateuser(user_id:int,db:Session = Depends(get_session), token=str):
    return controller.deleteUsercontroller(db,token, user_id)

@router.post("/logout/{user_id}", response_model=updateuserresponse, summary="logout User", description="User can logout in this endpoint", tags=["User"] )
async def updateuser(user_id:int,db:Session = Depends(get_session), token=str):
    return controller.logoutusercontroller(db,user_id,token)


