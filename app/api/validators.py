from http import HTTPStatus
from typing import Optional
from app.api.constants import (CANNOT_LIKE_OWN_POST, EMAIL_ALREADY_EXISTS,
                               LIKE_ALREADY_EXISTS, NOT_FOUND_LIKE,
                               NOT_FOUND_POST, NOT_OWNER)
from app.crud.post import post_crud
from app.crud.user import user_crud
from app.models import User
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def check_post_exists(
        post_id: int,
        session: AsyncSession
) -> Optional[dict]:
    """
    Проверяет существование поста с указанным идентификатором.
    :param post_id: Идентификатор поста для проверки.
    :param session: Асинхронная сессия SQLAlchemy.
    :raises HTTPException: Если пост не найден.
    :return: Объект поста (dict) или None, если пост не найден.
    """
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
) -> dict:
    """
    Проверяет, является ли пользователь владельцем поста.
    :param post_id: Идентификатор поста для проверки.
    :param session: Асинхронная сессия SQLAlchemy.
    :param user: Объект пользователя.
    :raises HTTPException: Если пользователь не является владельцем поста.
    :return: Объект поста (dict).
    """
    post = await post_crud.get_object(post_id, session)
    if post.user_id != user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=NOT_OWNER
        )
    return post


async def check_like_exists(
        post_id: int,
        user_id: int,
        session: AsyncSession
) -> dict:
    """
    Проверяет существование лайка от указанного пользователя на указанном посте.
    :param post_id: Идентификатор поста для проверки лайка.
    :param user_id: Идентификатор пользователя для проверки лайка.
    :param session: Асинхронная сессия SQLAlchemy.
    :raises HTTPException: Если лайк не найден.
    :return: Объект лайка (dict).
    """
    like = await post_crud.get_like_by_user_and_post_id(post_id, user_id, session)
    if not like:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NOT_FOUND_LIKE
        )
    return like


async def check_not_liking_own_post(
        post_id: int,
        user: User,
        session: AsyncSession
) -> dict:
    """
    Проверяет, что пользователь не может лайкать свои собственные посты.
    :param post_id: Идентификатор поста для проверки.
    :param user: Объект пользователя.
    :param session: Асинхронная сессия SQLAlchemy.
    :raises HTTPException: Если пользователь пытается лайкнуть свой собственный пост.
    :return: Объект поста (dict).
    """
    post = await post_crud.get_object(post_id, session)
    if post.user_id == user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=CANNOT_LIKE_OWN_POST
        )
    return post


async def check_on_duplicate_like(
        post_id: int,
        user: User,
        session: AsyncSession
) -> Optional[dict]:
    """
    Проверяет наличие дубликата лайка от указанного пользователя на указанном посте.
    :param post_id: Идентификатор поста для проверки лайка.
    :param user: Объект пользователя.
    :param session: Асинхронная сессия SQLAlchemy.
    :raises HTTPException: Если лайк от указанного пользователя на указанном посте уже существует.
    :return: Объект лайка (dict) или None, если лайк не найден.
    """
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
) -> Optional[dict]:
    """
    Проверяет наличие дубликата email в базе данных.
    :param email: Email для проверки.
    :param session: Асинхронная сессия SQLAlchemy.
    :raises HTTPException: Если email уже существует в базе данных.
    :return: Объект пользователя (dict) или None, если email не найден.
    """
    check_email = await user_crud.email_exists_in_db(email, session)
    if check_email is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=EMAIL_ALREADY_EXISTS
        )
    return check_email

