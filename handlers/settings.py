from aiogram import types, F
from core.dispatcher import dp
from keyboards.language_kb import language_keyboard
from keyboards.forecast_kb import forecast_keyboard
from keyboards.settings_kb import settings_keyboard
from keyboards.notification_time_kb import notification_time_keyboard
from services.weather_service import get_weather
from utils.state import user_languages, user_cities, user_notifications, persist_state


def build_settings_text(user_id: int) -> str:
    """Создаёт текст с текущими настройками пользователя"""
    lang = user_languages.get(user_id, "ru")
    city = user_cities.get(user_id, "—")
    notif = user_notifications.get(user_id, {"enabled": False, "hour": None})

    lang_text = "Русский 🇷🇺" if lang == "ru" else "O‘zbek 🇺🇿"
    notif_text = (
        f"Ежедневно в {notif['hour']:02d}:00" if notif.get("enabled") else "Отключена"
    )

    if lang == "ru":
        return (
            f"<b>⚙️ Ваши текущие настройки:</b>\n\n"
            f"🌐 Язык: {lang_text}\n"
            f"🏙 Город: {city}\n"
            f"🔔 Рассылка: {notif_text}"
        )
    else:
        return (
            f"<b>⚙️ Joriy sozlamalaringiz:</b>\n\n"
            f"🌐 Til: {lang_text}\n"
            f"🏙 Shahar: {city}\n"
            f"🔔 Xabarnoma: {notif_text}"
        )


# --- Открытие настроек ---
@dp.callback_query(F.data == "settings")
async def open_settings(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    notif = user_notifications.get(user_id, {"enabled": False})

    await callback.message.edit_text(
        build_settings_text(user_id),
        parse_mode="HTML",
        reply_markup=settings_keyboard(lang, has_notifications=notif.get("enabled"))
    )


# --- Включение рассылки ---
@dp.callback_query(F.data == "enable_notifications")
async def enable_notifications(callback: types.CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "ru")
    text = (
        "🕓 Когда хотите получать прогноз?" if lang == "ru"
        else "🕓 Qachon ob-havo ma’lumotini olishni xohlaysiz?"
    )
    await callback.message.edit_text(text, reply_markup=notification_time_keyboard())


# --- Установка времени рассылки ---
@dp.callback_query(F.data.startswith("set_time_"))
async def set_notification_time(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")

    selected_hour = int(callback.data.split("_")[2])
    user_notifications[user_id] = {"enabled": True, "hour": selected_hour}
    persist_state()  # 💾 сохраняем настройки

    text = (
        f"✅ Рассылка включена! Прогноз будет приходить каждый день в {selected_hour:02d}:00."
        if lang == "ru"
        else f"✅ Xabarnoma yoqildi! Siz har kuni soat {selected_hour:02d}:00 da ob-havo ma’lumotini olasiz."
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(text)

    await callback.message.answer(
        build_settings_text(user_id),
        parse_mode="HTML",
        reply_markup=settings_keyboard(lang, has_notifications=True)
    )


# --- Изменить время рассылки ---
@dp.callback_query(F.data == "change_time")
async def change_time(callback: types.CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "ru")
    text = (
        "🕓 Выберите новое время для рассылки:" if lang == "ru"
        else "🕓 Xabarnoma uchun yangi vaqtni tanlang:"
    )
    await callback.message.edit_text(text, reply_markup=notification_time_keyboard())


# --- Отключить рассылку ---
@dp.callback_query(F.data == "disable_notifications")
async def disable_notifications(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")

    user_notifications[user_id] = {"enabled": False, "hour": None}
    persist_state()  # 💾 сохраняем отключение

    text = (
        "🔕 Рассылка отключена." if lang == "ru"
        else "🔕 Xabarnoma o‘chirildi."
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(text)

    await callback.message.answer(
        build_settings_text(user_id),
        parse_mode="HTML",
        reply_markup=settings_keyboard(lang, has_notifications=False)
    )


# --- Кнопка «Назад» ---
@dp.callback_query(F.data == "back_to_forecast")
async def back_to_menu(callback: types.CallbackQuery):
    """Возврат к выбору прогноза"""
    lang = user_languages.get(callback.from_user.id, "ru")

    text = (
        "Какой прогноз вы хотели бы получить?" if lang == "ru"
        else "Qaysi prognozni olishni xohlaysiz?"
    )

    await callback.message.edit_text(
        f"<b>{text}</b>",
        parse_mode="HTML",
        reply_markup=forecast_keyboard(lang)
    )
