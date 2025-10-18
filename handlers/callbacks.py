from aiogram import Router, types, F
from services.weather_service import get_weather, get_forecast_3days
from keyboards.forecast_kb import forecast_keyboard
from utils.state import user_languages, user_cities

router = Router()


@router.callback_query(F.data == "change_lang")
async def change_lang(callback: types.CallbackQuery):
    await callback.message.answer("🌐 Изменение языка")
    await callback.answer()


@router.callback_query(F.data == "change_city")
async def change_city(callback: types.CallbackQuery):
    await callback.message.answer("🏙 Введите новый город")
    await callback.answer()


@router.callback_query(F.data == "change_time")
async def change_time(callback: types.CallbackQuery):
    await callback.message.answer("⏰ Изменение времени рассылки")
    await callback.answer()


@router.callback_query(F.data == "enable_notifications")
async def enable_notifications(callback: types.CallbackQuery):
    await callback.message.answer("🔔 Рассылка включена!")
    await callback.answer()


@router.callback_query(F.data == "disable_notifications")
async def disable_notifications(callback: types.CallbackQuery):
    await callback.message.answer("🔕 Рассылка отключена!")
    await callback.answer()


@router.callback_query(F.data == "back_to_forecast")
async def back_to_forecast(callback: types.CallbackQuery):
    await callback.message.answer("⬅️ Возвращаюсь к прогнозу погоды 🌦️")
    await callback.answer()


# --- Прогноз на сегодня ---
@router.callback_query(F.data == "forecast_today")
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
@router.callback_query(F.data == "forecast_3days")
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
