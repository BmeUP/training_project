from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from src.pydantic_models.user import UserPY
from src.db.models.user import User
from src.users.services.utils import validate_phone, validate_email, hash_password


class UserSignUp:
    def __init__(self, user_data: UserPY, db_session) -> None:
        self.user_data = user_data
        self.db_session = db_session
    
    async def sign_up(self):
        self._validate_phone()
        self._validate_email()
        
        async with self.db_session as s:
            user_db = User(name=self.user_data.name, email=self.user_data.email, 
                           phone=self.user_data.phone, password=hash_password(self.user_data.password))
            s.add(user_db)

            try:
                await s.commit()
                return JSONResponse({"message": f"User {self.user_data.name} is signed up!"}, status_code=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return JSONResponse(content={"message": "User with this phone or email already exists."}, status_code=status.HTTP_409_CONFLICT)
    
    def _validate_phone(self):
        phone_is_valid = validate_phone(self.user_data.phone)

        if phone_is_valid:
            return True
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone is invalid!")

    def _validate_email(self):
        email_is_valid = validate_email(self.user_data.email)

        if email_is_valid:
            return True
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is invalid!")
