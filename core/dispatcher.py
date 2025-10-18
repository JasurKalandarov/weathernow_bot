from aiogram import Dispatcher

# Импортируем роутеры
from handlers.start import router as start_router
from handlers.weather import router as weather_router
from handlers.settings import router as settings_router
from handlers.callbacks import router as callbacks_router

# Создаём диспетчер
dp = Dispatcher()

# Подключаем все роутеры
dp.include_router(start_router)
dp.include_router(weather_router)
dp.include_router(settings_router)
dp.include_router(callbacks_router)
