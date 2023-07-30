from app.core.db import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель для хранения данных о пользователе.
    """
    username = Column(String, nullable=False, unique=True, index=True)
    liked_posts = relationship("PostLike", backref="liked_by_user")
