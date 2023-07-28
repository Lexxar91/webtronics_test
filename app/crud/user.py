from sqlalchemy import select, func, bindparam
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import User, PostLike


class CRUDUser(CRUDBase):
    @classmethod
    async def get_my_likes_count(
            cls,
            user: User,
            session: AsyncSession
    ):
        stmt = select(func.count()).where(PostLike.user_id == bindparam('user_id', user.id))
        result = await session.execute(stmt)
        likes_count = result.scalar()
        return likes_count

    @classmethod
    async def email_exists_in_db(
            cls,
            email: str,
            session: AsyncSession
    ):
        result = await session.execute(
            select(User).options(
                selectinload(User.email)
            ).where(User.email == email)
        )
        user = result.scalars().first()
        return user


user_crud = CRUDUser(User)
