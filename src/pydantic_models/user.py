from pydantic import BaseModel


class UserPY(BaseModel):
    name: str
    email: str
    phone: str
    password: str


class SignInUser(BaseModel):
    email: str
    password: str