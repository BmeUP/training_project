from pydantic import BaseModel


class JWTToken(BaseModel):
    token: str