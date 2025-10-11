import aiohttp
from datetime import datetime
from config import WEATHER_API

MONTHS_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

MONTHS_UZ = {
    1: "yanvar", 2: "fevral", 3: "mart", 4: "aprel",
    5: "may", 6: "iyun", 7: "iyul", 8: "avgust",
    9: "sentyabr", 10: "oktyabr", 11: "noyabr", 12: "dekabr"
}


# --- Основной текущий прогноз ---
async def get_weather(city: str, lang: str = "ru") -> str:
    try:
        url = (
            f"http://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={WEATHER_API}&units=metric&lang={lang}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        if data.get("cod") != 200:
            return (
                "❌ Город не найден. Попробуй ещё раз."
                if lang == "ru"
                else "❌ Shahar topilmadi. Qayta urinib ko‘ring."
            )

        city_name = data["name"]
        temp = round(data["main"]["temp"])
        feels_like = round(data["main"]["feels_like"])
        description = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind = round(data["wind"]["speed"])
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.fromtimestamp(data["sys"]["sunset"])

        icon_map = {
            "ясно": "☀️", "пасмурно": "☁️", "небольшой дождь": "🌦",
            "дождь": "🌧", "снег": "❄️", "гроза": "⛈", "туман": "🌫"
        }
        icon = icon_map.get(description.lower(), "🌤")

        today = datetime.now()
        month_name = MONTHS_UZ[today.month] if lang == "uz" else MONTHS_RU[today.month]
        date_str = f"{today.day} {month_name}"

        if lang == "ru":
            return (
                f"📍 <b>{city_name}</b>\n\n"
                f"📅 <b>Сегодня, {date_str}</b>\n"
                f"{icon} {description}\n\n"
                f"🌡 Температура: <b>{temp}°C</b>\n"
                f"🤔 Ощущается как: <b>{feels_like}°C</b>\n"
                f"💧 Влажность: <b>{humidity}%</b>\n"
                f"💨 Ветер: <b>{wind} м/с</b>\n\n"
                f"🌅 Восход: <b>{sunrise.strftime('%H:%M')}</b>\n"
                f"🌇 Закат: <b>{sunset.strftime('%H:%M')}</b>"
            )
        else:
            return (
                f"📍 <b>{city_name}</b>\n\n"
                f"📅 <b>Bugun, {date_str}</b>\n"
                f"{icon} {description}\n\n"
                f"🌡 Harorat: <b>{temp}°C</b>\n"
                f"🤔 His qilinadi: <b>{feels_like}°C</b>\n"
                f"💧 Namlik: <b>{humidity}%</b>\n"
                f"💨 Shamol: <b>{wind} m/s</b>\n\n"
                f"🌅 Quyosh chiqishi: <b>{sunrise.strftime('%H:%M')}</b>\n"
                f"🌇 Quyosh botishi: <b>{sunset.strftime('%H:%M')}</b>"
            )

    except Exception as e:
        print(f"⚠️ Ошибка погоды: {e}")
        return (
            "⚠️ Ошибка при получении данных о погоде."
            if lang == "ru"
            else "⚠️ Ob-havo ma’lumotida xatolik yuz berdi."
        )


# --- Прогноз на 3 дня ---
async def get_forecast_3days(city: str, lang: str = "ru") -> str:
    """Возвращает прогноз погоды на 3 дня вперёд"""
    try:
        url = (
            f"http://api.openweathermap.org/data/2.5/forecast?"
            f"q={city}&appid={WEATHER_API}&units=metric&lang={lang}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        if data.get("cod") != "200":
            return (
                "❌ Город не найден. Попробуй ещё раз."
                if lang == "ru"
                else "❌ Shahar topilmadi. Qayta urinib ko‘ring."
            )

        city_name = data["city"]["name"]
        forecasts = data["list"]

        # Берем по одному прогнозу в день (12:00)
        daily = []
        for item in forecasts:
            if "12:00:00" in item["dt_txt"]:
                daily.append(item)
            if len(daily) >= 3:
                break

        lines = []
        for f in daily:
            date = datetime.fromtimestamp(f["dt"])
            temp = round(f["main"]["temp"])
            desc = f["weather"][0]["description"].capitalize()
            icon = {
                "ясно": "☀️", "пасмурно": "☁️", "небольшой дождь": "🌦",
                "дождь": "🌧", "снег": "❄️", "гроза": "⛈", "туман": "🌫"
            }.get(desc.lower(), "🌤")

            month_name = MONTHS_UZ[date.month] if lang == "uz" else MONTHS_RU[date.month]
            date_str = f"{date.day} {month_name}"

            if lang == "ru":
                lines.append(f"📅 <b>{date_str}</b> — {icon} {desc}, <b>{temp}°C</b>")
            else:
                lines.append(f"📅 <b>{date_str}</b> — {icon} {desc}, <b>{temp}°C</b>")

        header = (
            f"🌦 <b>Прогноз на 3 дня для {city_name}:</b>"
            if lang == "ru"
            else f"🌦 <b>{city_name} uchun 3 kunlik prognoz:</b>"
        )

        return f"📍 <b>{city_name}</b>\n\n{header}\n\n" + "\n".join(lines)

    except Exception as e:
        print(f"⚠️ Ошибка прогноза: {e}")
        return (
            "⚠️ Не удалось получить прогноз на 3 дня."
            if lang == "ru"
            else "⚠️ 3 kunlik prognoz olinmadi."
        )
