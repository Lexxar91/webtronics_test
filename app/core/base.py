"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base  # noqa
from app.models.user import  User # noqa
from app.models.post import Post, PostLike # noqa