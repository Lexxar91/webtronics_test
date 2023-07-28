from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_post_exists, check_post_owner, check_like_exists, check_not_liking_own_post, \
    check_on_duplicate_like
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.user import user_crud
from app.models import User
from app.schemas.post import PostCreate, PostInDB, PostUpdate, PostLikeInDB
from app.crud.post import post_crud
from app.schemas.user import UserLikesResponse

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
    dependencies=[Depends(current_user)]
)
async def get_all_posts(session: AsyncSession = Depends(get_async_session)):
    all_posts = await post_crud.get_all_objects(session)
    return all_posts


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
):
    post = await check_post_exists(post_id, session)
    await check_post_owner(post_id, session, user)
    await post_crud.update_object(
        post,
        obj_in,
        session
    )



@router.delete(
    '{post_id}',
    status_code=HTTPStatus.NO_CONTENT,
    response_model_exclude_none=True
)
async def delete_post(
        post_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
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
):
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
):
    await check_post_exists(post_id, session)
    await check_like_exists(post_id, user.id, session)
    print(user.id)
    await post_crud.remove_like(post_id, user, session)


@router.get(
    '/my_likes',
    response_model=UserLikesResponse
)
async def get_count_my_like(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    count_like = await user_crud.get_my_likes_count(user, session)
    return UserLikesResponse(my_likes_count=count_like)

