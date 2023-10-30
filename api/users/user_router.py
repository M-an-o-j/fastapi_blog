from fastapi import APIRouter, Depends
from api.users.user_schema import UserResponse, Userlogin, loginresponse, updateuserresponse, UserSignUp
from sqlalchemy.orm import Session
from Database import get_session
from api.users.user_controller import user_controller

router = APIRouter()

controller = user_controller()

@router.post("/signup", response_model=UserResponse, summary="Create an user",description="Using this endpoint to create an user here", tags=["User"])
async def signup(user: UserSignUp , db: Session = Depends(get_session) ):
    return controller.createUsercontroller(db, user)

@router.post("/signin", response_model=loginresponse, summary="Login User", description="User can login here", tags=["User"])
async def signin(user: Userlogin, db:Session = Depends(get_session)):
    return controller.loginusercontroller(db, user)

@router.put("/update/{user_id}", response_model=updateuserresponse, summary="Update User", description="User can update their details here", tags=["User"] )
async def updateuser(user: updateuserresponse, db:Session = Depends(get_session),user_id=int, token=str):
    return controller.updateUsercontroller(db, user,user_id, token)

@router.delete("/delete/{user_id}", response_model=updateuserresponse, summary="Delete User", description="User can  their details here", tags=["User"] )
async def updateuser(user_id:str ,db:Session = Depends(get_session), token=str):
    return controller.deleteUsercontroller(db,token, user_id)
