from fastapi_users import schemas
from pydantic import Field, BaseModel


class UserRead(schemas.BaseUser[int]):
    """
    Схема данных для чтения информации о пользователе.
    """
    username: str


class UserCreate(schemas.BaseUserCreate):
    """
    Схема данных для создания нового пользователя.
    """
    username: str = Field(..., min_length=3, max_length=50)


class UserUpdate(schemas.BaseUserUpdate):
    """
    Схема данных для обновления информации о пользователе.
    """
    pass


class UserLikesResponse(BaseModel):
    """
    Схема данных для представления количества лайков у пользователя.
    """
    my_likes_count: int
