from http import HTTPStatus
from typing import List
from app.api.validators import (check_like_exists, check_not_liking_own_post,
                                check_on_duplicate_like, check_post_exists,
                                check_post_owner)
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.post import post_crud
from app.crud.user import user_crud
from app.models import User
from app.schemas.post import PostCreate, PostInDB, PostLikeInDB, PostUpdate
from app.schemas.user import UserLikesResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    '/',
    response_model=PostInDB,
    response_model_exclude_none=True,
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(current_user)]
)
async def create_new_post(
        post: PostCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> PostInDB:
    """
    Создание нового поста.
    :param post: Данные нового поста из схемы PostCreate.
    :param user: Текущий авторизованный пользователь.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Созданный пост в формате PostInDB.
    """
    new_post = await post_crud.create_object(post, session, user)
    return new_post


@router.get(
    '/',
    response_model=List[PostInDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_all_posts(session: AsyncSession = Depends(get_async_session)) -> List[PostInDB]:
    """
    Получение всех постов.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Список всех постов в формате List[PostInDB].
    """
    all_posts = await post_crud.get_all_objects(session)
    return all_posts


@router.get(
    '{post_id}',
    response_model=PostInDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_post(
        post_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> PostInDB:
    """
    Получение информации о конкретном посте.
    :param post_id: Идентификатор поста для получения информации.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Информация о посте в формате PostInDB.
    """
    post = await post_crud.get_object(post_id, session)
    return post


@router.patch(
    '{post_id}',
    response_model_exclude_none=True,
    status_code=HTTPStatus.NO_CONTENT
)
async def update_post(
        post_id: int,
        obj_in: PostUpdate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> None:
    """
    Обновление существующего поста.
    :param post_id: Идентификатор поста, который нужно обновить.
    :param obj_in: Данные для обновления из схемы PostUpdate.
    :param session: Асинхронная сессия SQLAlchemy.
    :param user: Текущий авторизованный пользователь.
    """
    post = await check_post_exists(post_id, session)
    await check_post_owner(post_id, session, user)
    await post_crud.update_object(post, obj_in, session)


@router.delete(
    '{post_id}',
    status_code=HTTPStatus.NO_CONTENT,
    response_model_exclude_none=True
)
async def delete_post(
        post_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> None:
    """
    Удаление существующего поста.
    :param post_id: Идентификатор поста, который нужно удалить.
    :param session: Асинхронная сессия SQLAlchemy.
    :param user: Текущий авторизованный пользователь.
    """
    post = await check_post_owner(post_id, session, user)
    post = await check_post_exists(post.id, session)
    await post_crud.delete_object(post, session)


@router.post(
    '{post_id}/like',
    status_code=HTTPStatus.CREATED,
    response_model=PostLikeInDB,
    response_model_exclude_none=True,
)
async def post_like(
        post_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> PostLikeInDB:
    """
    Поставить лайк на пост.
    :param post_id: Идентификатор поста, на который нужно поставить лайк.
    :param user: Текущий авторизованный пользователь.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Объект PostLikeInDB - информация о лайке.
    """
    await check_post_exists(post_id, session)
    await check_not_liking_own_post(post_id, user, session)
    await check_on_duplicate_like(post_id, user, session)
    like = await post_crud.put_a_like(post_id, user, session)
    return like


@router.delete(
    '{post_id}/remove_like',
    status_code=HTTPStatus.NO_CONTENT
)
async def remove_post_like(
        post_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> None:
    """
    Удалить лайк с поста.
    :param post_id: Идентификатор поста, с которого нужно удалить лайк.
    :param user: Текущий авторизованный пользователь.
    :param session: Асинхронная сессия SQLAlchemy.
    """
    await check_post_exists(post_id, session)
    await check_like_exists(post_id, user.id, session)
    await post_crud.remove_like(post_id, user, session)


@router.get(
    '/my_likes',
    response_model=UserLikesResponse
)
async def get_count_my_like(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> UserLikesResponse:
    """
    Получить количество лайков текущего пользователя.
    :param user: Текущий авторизованный пользователь.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Объект UserLikesResponse - количество лайков пользователя.
    """
    count_like = await user_crud.get_my_likes_count(user, session)
    return UserLikesResponse(my_likes_count=count_like)
