from typing import Generator, Optional, Union
from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.utils import check_email_async
from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> Generator:
    """
    Функция зависимости для получения базы данных пользователей.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Генератор SQLAlchemyUserDatabase.
    """
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """
    Функция получения стратегии аутентификации JWT.
    :return: JWTStrategy.
    """
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self,
        password: str,
        user: UserCreate
    ) -> None:
        """
        Проверка пароля при регистрации пользователя.
        :param password: Пароль, который нужно проверить.
        :param user: Объект UserCreate с данными пользователя.
        :raises InvalidPasswordException: Если пароль не проходит проверку.
        """
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ) -> None:
        """
        Вызывается после успешной регистрации пользователя.
        :param user: Объект User, представляющий пользователя.
        :param request: Запрос FastAPI, если применимо.
        """
        print(f'Пользователь {user.email} зарегистрирован.')

    async def create(self, user: UserCreate, **kwargs) -> User:
        """
        Создание пользователя.
        :param user: Объект UserCreate с данными пользователя.
        :param kwargs: Дополнительные параметры (не используются в данном контексте).
        :return: Созданный объект User.
        """
        response = await check_email_async(user.email)
        if response["result"] == "deliverable":
            print("Email exists")
        elif response["result"] == "undeliverable":
            print("Email does not exist")
        else:
            print("Unable to verify email")
        user_data = user.dict()
        user_data.pop("password", None)
        return await super().create(user, **kwargs)


async def get_user_manager(user_db: SQLAlchemyUserDatabase[User, int] = Depends(get_user_db)) -> Generator:
    """
    Функция зависимости для получения менеджера пользователей.
    :param user_db: База данных пользователей.
    :return: Генератор UserManager.
    """
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user: Union[User, None] = fastapi_users.current_user(active=True)
current_superuser: Union[User, None] = fastapi_users.current_user(active=True, superuser=True)
