from datetime import datetime, timezone
from app.core.db import Base
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text
)


class Post(Base):
    """
    Модель для хранения данных о посте пользователя.
    """
    user_id = Column(Integer, ForeignKey('user.id'))
    text = Column(Text, nullable=False)
    username = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now(tz=timezone.utc))


class PostLike(Base):
    """
    Модель для хранения данных о лайке на пост.
    """
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc))
    index = Index('post_like_user_index', 'post_id', 'user_id')

