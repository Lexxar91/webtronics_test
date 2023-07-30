from typing import Optional
from app.crud.base import CRUDBase
from app.models import User
from app.models.post import Post, PostLike
from sqlalchemy import bindparam, select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDPost(CRUDBase):
    @classmethod
    async def put_a_like(
        cls,
        post_id: int,
        user: User,
        session: AsyncSession
    ) -> PostLike:
        """
        Поставить лайк на пост.
        :param post_id: Идентификатор поста, на который нужно поставить лайк.
        :param user: Объект пользователя, который ставит лайк.
        :param session: Асинхронная сессия SQLAlchemy.
        :return: Объект лайка (PostLike) - информация о лайке.
        """
        like = PostLike(
            post_id=post_id,
            user_id=user.id
        )
        session.add(like)
        await session.commit()
        await session.refresh(like)
        return like

    @classmethod
    async def remove_like(
        cls,
        post_id: int,
        user: User,
        session: AsyncSession
    ) -> Optional[PostLike]:
        """
        Удалить лайк с поста.
        :param post_id: Идентификатор поста, с которого нужно удалить лайк.
        :param user: Объект пользователя, который удаляет лайк.
        :param session: Асинхронная сессия SQLAlchemy.
        :return: Объект лайка (PostLike), если он был найден и удален, или None, если лайк не найден.
        """
        result = await session.execute(
            select(PostLike).where(
                PostLike.post_id == bindparam('post_id', post_id),
                PostLike.user_id == user.id
            )
        )
        like = result.scalars().first()
        await session.delete(like)
        await session.commit()
        return like

    @classmethod
    async def get_like_by_user_and_post_id(
        cls,
        post_id: int,
        user_id: int,
        session: AsyncSession
    ) -> Optional[PostLike]:
        """
        Проверяет существование лайка от указанного пользователя на указанном посте.
        :param post_id: Идентификатор поста для проверки лайка.
        :param user_id: Идентификатор пользователя для проверки лайка.
        :param session: Асинхронная сессия SQLAlchemy.
        :return: Объект лайка (PostLike), если он был найден, или None, если лайк не найден.
        """
        result = await session.execute(
            select(PostLike).where(
                PostLike.post_id == post_id,
                PostLike.user_id == user_id
            )
        )
        like = result.scalars().first()
        return like


post_crud = CRUDPost(Post)

