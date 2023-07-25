from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_post_exists, check_post_owner, check_like_exists, check_not_liking_own_post
from app.core.db import get_async_session
from app.core.user import current_user
from app.models import User
from app.schemas.post import PostCreate, PostInDB, PostUpdate, PostLikeInDB
from app.crud.post import post_crud

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
):
    new_post = await post_crud.create_object(post, session, user)
    return new_post


@router.get(
    '/',
    response_model=list[PostInDB],
    response_model_exclude_none=True,
    response_model_exclude_unset=True
)
async def get_all_posts(session: AsyncSession = Depends(get_async_session)):
    all_posts = await post_crud.get_all_objects(session)
    return all_posts


@router.patch(
    '{post_id}',
    response_model=PostInDB,
    response_model_exclude_none=True
)
async def update_post(
    post_id: int,
    obj_in: PostUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    post = await check_post_exists(post_id, session)
    post = await post_crud.update_object(
        post,
        obj_in,
        session
    )
    return post


@router.delete(
    '{post_id}',
    response_model=PostInDB,
    response_model_exclude_none=True
)
async def delete_post(
        post_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    await check_post_owner(post_id, session, user)
    post = await check_post_exists(post_id, session)
    post = await post_crud.delete_object(post, session)
    return post


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
):
    await check_post_exists(post_id, session)
    await check_not_liking_own_post(post_id, user, session)
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
):
    await check_post_exists(post_id, session)
    like = await check_like_exists(post_id, user, session)
    await post_crud.remove_like(like, session)
    #return removed_like
