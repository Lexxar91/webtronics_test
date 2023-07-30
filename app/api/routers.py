from fastapi import APIRouter
from app.api.endpoints import user_router, post_router

main_router = APIRouter()


# Включение маршрута API для работы с пользователями
main_router.include_router(user_router)

# Включение маршрута API для работы с постами, с префиксом '/Post' и тегом 'Posts'
main_router.include_router(
    post_router,
    prefix='/Post',
    tags=['Posts']
)
