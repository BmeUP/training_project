from datetime import datetime, timedelta

from jose import jwt

from settings import settings
from src.pydantic_models.jwt import JWTToken as JWTTokenModel


class JWTToken:
    def __init__(self, data: dict | None = None, token: str | None = None) -> None:
        self.secrete_key = settings.salt
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 5
        self.data = data
        self.token = token
    
    def create_access_token(self):
        to_encode = self.data.copy()
        to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)})
        encoded_jwt = jwt.encode(to_encode, self.secrete_key, algorithm=self.algorithm)
        return JWTTokenModel(token=encoded_jwt)

    def verifvy_token(self):
        return jwt.decode(self.token, key=self.secrete_key, algorithms=[self.algorithm])