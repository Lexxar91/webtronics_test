from datetime import datetime, timezone

from sqlalchemy import Column, Text, Integer, ForeignKey, String, DateTime, Index
from sqlalchemy.orm import relationship

from app.core.db import Base


class Post(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    text = Column(Text, nullable=False)
    username = Column(String, nullable=False, index=True)
    create_date = Column(DateTime, nullable=False, default=datetime.now(tz=timezone.utc))


class PostLike(Base):
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc))
    index = Index('post_like_user_index', 'post_id', 'user_id')

