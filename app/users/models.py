from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class BaseUser(BaseModel):
    username: str
    password: str


class CreateUser(BaseUser):
    password: str


class User(BaseUser):
    id: PyObjectId = Field(alias="_id", default=None)


class Login(BaseUser):
    password: str
