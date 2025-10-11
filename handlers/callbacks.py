from aiogram import types, F
from core.dispatcher import dp
from services.weather_service import get_weather, get_forecast_3days
from keyboards.forecast_kb import forecast_keyboard
from utils.state import user_languages, user_cities


# --- Прогноз на сегодня ---
@dp.callback_query(F.data == "forecast_today")
async def forecast_today(callback: types.CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "ru")
    city = user_cities.get(callback.from_user.id)

    if not city:
        text = "Сначала отправь название города 🌆" if lang == "ru" else "Avval shahar nomini yuboring 🌆"
        await callback.message.answer(text)
        return

    try:
        await callback.message.delete()
    except:
        pass

    weather_info = await get_weather(city, lang)
    await callback.message.answer(weather_info, parse_mode="HTML")

    question_text = (
        "Какой прогноз вы хотели бы получить?" if lang == "ru"
        else "Qaysi prognozni olishni xohlaysiz?"
    )

    await callback.message.answer(
        f"<b>{question_text}</b>",
        parse_mode="HTML",
        reply_markup=forecast_keyboard(lang)
    )


# --- Прогноз на 3 дня ---
@dp.callback_query(F.data == "forecast_3days")
async def forecast_3days(callback: types.CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "ru")
    city = user_cities.get(callback.from_user.id)

    if not city:
        text = "Сначала отправь название города 🌆" if lang == "ru" else "Avval shahar nomini yuboring 🌆"
        await callback.message.answer(text)
        return

    try:
        await callback.message.delete()
    except:
        pass

    forecast_text = await get_forecast_3days(city, lang)
    await callback.message.answer(forecast_text, parse_mode="HTML")

    question_text = (
        "Какой прогноз вы хотели бы получить?" if lang == "ru"
        else "Qaysi prognozni olishni xohlaysiz?"
    )

    await callback.message.answer(
        f"<b>{question_text}</b>",
        parse_mode="HTML",
        reply_markup=forecast_keyboard(lang)
    )
