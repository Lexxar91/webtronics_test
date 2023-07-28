from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from app.api.constants import NOT_FOUND_POST, NOT_OWNER, NOT_FOUND_LIKE, CANNOT_LIKE_OWN_POST, LIKE_ALREADY_EXISTS, \
    EMAIL_ALREADY_EXISTS
from app.crud.post import post_crud
from app.crud.user import user_crud
from app.models import User


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
        user: User,
):
    post = await post_crud.get_object(post_id, session)
    if post.user_id != user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=NOT_OWNER
        )
    return post


async def check_like_exists(post_id, user_id, session):
    like = await post_crud.get_like_by_user_and_post_id(post_id, user_id, session)
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
    return post


async def check_on_duplicate_like(
        post_id,
        user,
        session: AsyncSession
):
    get_like = await post_crud.get_like_by_user_and_post_id(post_id, user.id, session)
    if get_like is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=LIKE_ALREADY_EXISTS
        )
    return get_like


async def check_on_duplicate_email_in_db(
        email,
        session: AsyncSession
):
    check_email = await user_crud.email_exists_in_db(email, session)
    if check_email is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=EMAIL_ALREADY_EXISTS
        )
    return check_email

