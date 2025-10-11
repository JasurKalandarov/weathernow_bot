from aiogram import types
from aiogram import Bot
from core.dispatcher import dp
from services.weather_service import get_weather
from utils.state import user_languages, last_messages, user_cities, persist_state
from keyboards.forecast_kb import forecast_keyboard
from utils.delete import delete_previous


@dp.message()
async def handle_city(message: types.Message, bot: Bot):
    await delete_previous(bot, message.chat.id, message.from_user.id)

    city = message.text.strip()
    user_cities[message.from_user.id] = city
    persist_state()  # 💾 сохраняем город

    lang = user_languages.get(message.from_user.id, "ru")

    question_text = (
        "Какой прогноз вы хотели бы получить?" if lang == "ru"
        else "Qaysi prognozni olishni xohlaysiz?"
    )

    msg = await message.answer(
        f"✅ <b>{'Город сохранён' if lang == 'ru' else 'Shahar saqlandi'}</b>\n\n"
        f"<b>{question_text}</b>",
        parse_mode="HTML",
        reply_markup=forecast_keyboard(lang)
    )
    last_messages[message.from_user.id] = msg.message_id
    persist_state()  # 💾 сохраняем последнее сообщение
