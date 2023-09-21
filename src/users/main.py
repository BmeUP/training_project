from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.pydantic_models.user import UserPY, SignInUser
from src.db.main import get_db
from src.users.services.sign_up import UserSignUp
from src.users.services.sign_in import UserSignIn

user_router = APIRouter(prefix="/user")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@user_router.post("/sign-up")
async def sign_up(user: UserPY, session: Session = Depends(get_db)):
    user_signup = UserSignUp(user_data=user, db_session=session)
    return await user_signup.sign_up()

@user_router.post("/sign-in")
async def sign_in(user: SignInUser, session: Session = Depends(get_db)):
    user_signin = UserSignIn(user_data=user, db_session=session)
    return await user_signin.try_login()
