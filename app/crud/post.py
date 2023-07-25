from sqlalchemy import select, literal
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User
from app.models.post import Post, PostLike
from app.schemas.post import PostCreate


class CRUDPost(CRUDBase):
    @classmethod
    async def put_a_like(
            cls,
            post_id: int,
            current_user: User,
            session: AsyncSession
    ):
        like = PostLike(
            post_id=post_id,
            user_id=current_user.id
        )
        session.add(like)
        await session.commit()
        await session.refresh(like)
        return like

    @classmethod
    async def remove_like(cls, post_id, user, session: AsyncSession):
        result = await session.execute(
            select(PostLike).where(
                PostLike.post_id == literal(post_id),
                PostLike.user_id == literal(user.id)
            )
        )
        like = result.scalars().first()
        await session.delete(like)
        await session.commit()
        return like



post_crud = CRUDPost(Post)

