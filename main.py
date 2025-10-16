import asyncio
import logging
from aiogram import Bot
from aiohttp import web
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


async def start_bot():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    await on_startup(bot)
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)


# -----------------------------
# Минимальный веб-сервер для Render
# -----------------------------
async def handle(request):
    return web.Response(text="✅ Bot is running")


async def run_web():
    app = web.Application()
    app.router.add_get("/", handle)
    port = 10000  # Render автоматически пробрасывает этот порт
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()
    print(f"🌐 Web server started on port {port}")


async def main():
    await asyncio.gather(start_bot(), run_web())


if __name__ == "__main__":
    asyncio.run(main())
