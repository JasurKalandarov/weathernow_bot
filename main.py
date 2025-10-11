import asyncio
import logging
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.dispatcher import dp
from config import BOT_TOKEN
from services.scheduler import send_daily_forecasts

import handlers.start
import handlers.weather
import handlers.callbacks
import handlers.settings


async def on_startup(bot: Bot):
    """
    Запуск планировщика рассылки
    """
    scheduler = AsyncIOScheduler()
    # Задача выполняется каждый час в 00 минут (можно поменять, например, каждые 5 минут для теста)
    scheduler.add_job(send_daily_forecasts, "cron", minute=0, args=[bot])
    scheduler.start()
    print("✅ Планировщик рассылки запущен")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    await on_startup(bot)

    print("✅ Планировщик рассылки запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
