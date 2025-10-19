import asyncio
from datetime import datetime
import pytz
from aiogram import Bot
from services.weather_service import get_weather
from utils.state import user_notifications, user_cities, user_languages


async def send_daily_forecasts(bot: Bot):
    """Проверяет пользователей и отправляет прогноз, если наступило их время"""
    # используем время Ташкента
    tashkent_tz = pytz.timezone("Asia/Tashkent")
    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    now_local = now_utc.astimezone(tashkent_tz)
    current_hour = now_local.hour

    for user_id, notif in user_notifications.items():
        if not notif.get("enabled"):
            continue

        # Проверяем, совпадает ли локальное время с временем пользователя
        if notif.get("hour") == current_hour:
            city = user_cities.get(user_id)
            lang = user_languages.get(user_id, "ru")

            if not city:
                continue

            forecast_text = await get_weather(city, lang)

            if lang == "ru":
                message = (
                    f"🌆 <b>{city}</b>\n\n"
                    f"☀️ <b>Ваш прогноз на сегодня:</b>\n\n"
                    f"{forecast_text}"
                )
            else:
                message = (
                    f"🌆 <b>{city}</b>\n\n"
                    f"☀️ <b>Bugungi ob-havo ma’lumoti:</b>\n\n"
                    f"{forecast_text}"
                )

            try:
                await bot.send_message(
                    user_id,
                    message,
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Ошибка при отправке прогноза пользователю {user_id}: {e}")