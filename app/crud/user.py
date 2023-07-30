from typing import Optional
from app.crud.base import CRUDBase
from app.models import PostLike, User
from sqlalchemy import bindparam, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDUser(CRUDBase):
    @classmethod
    async def get_my_likes_count(
        cls,
        user: User,
        session: AsyncSession
    ) -> int:
        """
        Получить количество лайков для указанного пользователя.
        :param user: Объект пользователя, для которого нужно получить количество лайков.
        :param session: Асинхронная сессия SQLAlchemy.
        :return: Количество лайков (int) для пользователя.
        """
        stmt = select(func.count()).where(PostLike.user_id == bindparam('user_id', user.id))
        result = await session.execute(stmt)
        likes_count = result.scalar()
        return likes_count

    @classmethod
    async def email_exists_in_db(
        cls,
        email: str,
        session: AsyncSession
    ) -> Optional[User]:
        """
        Проверяет наличие пользователя с указанным email в базе данных.
        :param email: Email пользователя для проверки.
        :param session: Асинхронная сессия SQLAlchemy.
        :return: Объект пользователя (User), если email существует в базе данных, или None, если пользователя нет.
        """

        statement = select(User).where(User.email == email)
        result = await session.execute(statement)

        user = result.scalars().first()
        return user


user_crud = CRUDUser(User)
