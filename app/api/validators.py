from fastapi import HTTPException
from sqlalchemy import select, literal

from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from app.api.constants import NOT_FOUND_POST, NOT_OWNER, NOT_FOUND_LIKE, CANNOT_LIKE_OWN_POST
from app.crud.post import post_crud
from app.core.user import current_user
from app.models import PostLike


async def check_post_exists(
        post_id: int,
        session: AsyncSession
):
    get_post = await post_crud.get_object(post_id, session)
    if get_post is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NOT_FOUND_POST
        )
    return get_post


async def check_post_owner(
        post_id: int,
        session: AsyncSession,
        user: current_user
):
    post = await post_crud.get_object(post_id, session)
    if post.user_id != user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=NOT_OWNER
        )
    return post


async def check_like_exists(post_id, user, session):
    like = await post_crud.remove_like(post_id, user, session)
    if not like:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NOT_FOUND_LIKE
        )
    return like


async def check_not_liking_own_post(post_id, user, session):
    post = await post_crud.get_object(post_id, session)
    if post.user_id == user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=CANNOT_LIKE_OWN_POST
        )
    return True
