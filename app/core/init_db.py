import contextlib

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate
from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

# Превращаем асинхронные генераторы в асинхронные менеджеры контекста.
get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


# Корутина, создающая юзера с переданным email и паролем.
# Возможно создание суперюзера при передаче аргумента is_superuser=True.
async def create_user(
        email: EmailStr,
        password: str,
        is_superuser: bool = False,
        username: str = 'Lexxar'
):
    try:
        # Получение объекта асинхронной сессии.
        async with get_async_session_context() as session:
            # Получение объекта класса SQLAlchemyUserDatabase.
            async with get_user_db_context(session) as user_db:
                # Получение объекта класса UserManager.
                async with get_user_manager_context(user_db) as user_manager:
                    # Создание пользователя.
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                            username=username
                        )
                    )
    # В случае, если такой пользователь уже есть, ничего не предпринимать.
    except UserAlreadyExists:
        pass


async def create_first_superuser() -> None:
    """
    Создает первого суперпользователя при наличии данных в настройках.
    Если в настройках указан email и пароль первого суперпользователя, функция использует
    эти данные для создания суперпользователя.
    :return: None
    """
    if (settings.first_superuser_email is not None
            and settings.first_superuser_password is not None):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
