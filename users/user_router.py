from fastapi import APIRouter, Depends
from users.user_schema import UserResponse, Userlogin, loginresponse
from sqlalchemy.orm import Session
from Database import get_session
from users.user_controller import createUser, loginuser

router = APIRouter()

@router.post("/user/signup", response_model=UserResponse, summary="Create an user",description="Using this endpoint to create an user here", tags=["User"])
async def signup(user: UserResponse , db: Session = Depends(get_session) ):
    return createUser(db, user)

@router.post("/user/signin", response_model=loginresponse, summary="Login User", description="User can login here", tags=["User"])
async def signin(user: Userlogin, db:Session = Depends(get_session)):
    return loginuser(db, user)