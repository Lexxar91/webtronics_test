from pydantic import BaseModel, Field, Extra


class PostBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)

    class Config:
        extra = Extra.forbid


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostInDB(PostBase):
    id: int
    username: str

    class Config:
        orm_mode = True


class PostLikeBase(BaseModel):
    post_id: int
    user_id: int


class PostLikeCreate(PostLikeBase):
    pass


class PostLikeInDB(PostLikeBase):
    class Config:
        orm_mode = True
