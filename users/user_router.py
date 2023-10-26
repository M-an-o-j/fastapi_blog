from fastapi import APIRouter, Depends
from users.user_schema import UserResponse, Userlogin, loginresponse
from sqlalchemy.orm import Session
from Database import get_session
from users.user_controller import createUser, loginuser

router = APIRouter()

@router.post("/users/register", response_model=UserResponse)
async def createuser(user: UserResponse , db: Session = Depends(get_session) ):
    return createUser(db, user)

@router.post("/user/login", response_model=loginresponse)
async def loginUser(user: Userlogin, db:Session = Depends(get_session)):
    # print(**user.dict())
    return loginuser(db, user)