from app.core.config import settings
from app.api.routers import main_router
from app.core.init_db import create_first_superuser
from fastapi import FastAPI


app = FastAPI(title=settings.app_title)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    """
    Функция, выполняющаяся при запуске приложения.
    Вызывает создание первого суперпользователя, если указаны его email и пароль в настройках приложения.
    """
    await create_first_superuser()
