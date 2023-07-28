from sqlalchemy import select, literal, exists, and_, bindparam
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User
from app.models.post import Post, PostLike


class CRUDPost(CRUDBase):
    @classmethod
    async def put_a_like(
            cls,
            post_id: int,
            user: User,
            session: AsyncSession
    ):
        like = PostLike(
            post_id=post_id,
            user_id=user.id
        )
        session.add(like)
        await session.commit()
        await session.refresh(like)
        return like

    @classmethod
    async def remove_like(cls, post_id, user, session: AsyncSession):
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
    ):
        result = await session.execute(
            select(PostLike).where(
                PostLike.post_id == post_id,
                PostLike.user_id == user_id
            )
        )

        like = result.scalars().first()
        return like

post_crud = CRUDPost(Post)

