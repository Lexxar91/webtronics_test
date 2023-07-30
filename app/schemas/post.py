from pydantic import BaseModel, Field, Extra


class PostBase(BaseModel):
    """
    Базовая схема для данных поста.
    """
    text: str = Field(..., min_length=1, max_length=2000)

    class Config:
        extra = Extra.forbid


class PostCreate(PostBase):
    """
    Схема данных для создания нового поста.
    """
    pass


class PostUpdate(PostBase):
    """
    Схема данных для обновления существующего поста.
    """
    pass


class PostInDB(PostBase):
    """
    Схема данных для представления поста из базы данных.
    """
    username: str

    class Config:
        orm_mode = True


class PostLikeBase(BaseModel):
    """
    Базовая схема для данных лайка поста.
    """
    post_id: int
    user_id: int


class PostLikeCreate(PostLikeBase):
    """
    Схема данных для создания лайка на посте.
    """
    pass


class PostLikeInDB(PostLikeBase):
    """
    Схема данных для представления лайка поста из базы данных.
    """
    class Config:
        orm_mode = True