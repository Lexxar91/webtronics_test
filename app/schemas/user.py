from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    username: str


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(..., min_length=3, max_length=50)


class UserUpdate(schemas.BaseUserUpdate):
    pass