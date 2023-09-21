from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.pydantic_models.user import SignInUser
from src.db.models.user import User
from src.users.services.utils import check_passwords
from src.users.jwt.main import JWTToken


class UserSignIn():
    def __init__(self, user_data: SignInUser, db_session) -> None:
        self.user_data = user_data
        self.session = db_session
        self.db_user = None
    
    async def _get_user(self):
        async with self.session as s:
            stmt = select(User).where(User.email == self.user_data.email)
            try:
                result = await s.execute(stmt)
                self.db_user = result.scalars(stmt).one()
            except NoResultFound as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    
    async def try_login(self):
        await self._get_user()
        if not check_passwords(self.user_data.password, self.db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password!")

        jwt_obj = JWTToken({"email": self.db_user.email})

        return jwt_obj.create_access_token()
