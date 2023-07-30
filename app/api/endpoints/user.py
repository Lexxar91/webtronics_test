from app.api.constants import DELETE_USER_NOT_ALLOWED
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Маршрут для аутентификации через JWT
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
# Маршрут для регистрации новых пользователей
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
# Маршрут для работы с пользователями (получение, обновление и т.д.)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)


@router.delete(
    '/users/{id}',
    tags=['users'],
    deprecated=True
)
def delete_user(id: str):
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        status_code=405,
        detail=DELETE_USER_NOT_ALLOWED
    )
