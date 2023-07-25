from datetime import datetime, timezone

from sqlalchemy import Column, Text, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from app.core.db import Base


class Post(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    text = Column(Text, nullable=False)
    username = Column(String, nullable=False, index=True)
    create_date = Column(DateTime, nullable=False, default=datetime.now(tz=timezone.utc))
    likes = relationship("PostLike", backref="post_likes")


class PostLike(Base):
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc))


