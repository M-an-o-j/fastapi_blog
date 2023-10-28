from fastapi import APIRouter, Depends
from api.users.user_schema import UserResponse, Userlogin, loginresponse, updateuserresponse
from sqlalchemy.orm import Session
from Database import get_session
from api.users.user_controller import createUsercontroller, loginusercontroller, updateUsercontroller

router = APIRouter()

@router.post("/signup", response_model=UserResponse, summary="Create an user",description="Using this endpoint to create an user here", tags=["User"])
async def signup(user: UserResponse , db: Session = Depends(get_session) ):
    return createUsercontroller(db, user)

@router.post("/signin", response_model=loginresponse, summary="Login User", description="User can login here", tags=["User"])
async def signin(user: Userlogin, db:Session = Depends(get_session)):
    return loginusercontroller(db, user)

@router.put("/update/{token}", response_model=updateuserresponse, summary="Update User", description="User can their details here", tags=["User"] )
async def updateuser(user: updateuserresponse, db:Session = Depends(get_session), token=str):
    return updateUsercontroller(db, user, token)
