from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    username = Column(String, nullable=False, unique=True, index=True)
    liked_posts = relationship("PostLike", backref="liked_by_user")
