from aiogram import types, F
from aiogram.exceptions import TelegramBadRequest
from core.dispatcher import dp
from keyboards.language_kb import language_keyboard
from keyboards.forecast_kb import forecast_keyboard
from utils.state import user_languages, user_cities, persist_state


@dp.message(F.text == "/start")
async def handle_start(message: types.Message):
    user_id = message.from_user.id

    # Если язык и город уже сохранены — пропускаем выбор
    lang = user_languages.get(user_id)
    city = user_cities.get(user_id)

    if lang and city:
        question_text = (
            "Какой прогноз вы хотели бы получить?" if lang == "ru"
            else "Qaysi prognozni olishni xohlaysiz?"
        )
        await message.answer(
            f"👋 <b>С возвращением!</b>\n\n"
            f"<b>{question_text}</b>",
            parse_mode="HTML",
            reply_markup=forecast_keyboard(lang)
        )
        return

    # Если язык ещё не выбран
    text = "Пожалуйста, выберите язык / Iltimos, tilni tanlang:"
    await message.answer(text, reply_markup=language_keyboard())


@dp.callback_query(F.data.startswith("lang_"))
async def select_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    user_languages[callback.from_user.id] = lang
    persist_state()  # 💾 сохраняем язык

    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass

    text = (
        "Отправь мне название города, чтобы узнать погоду 🌤"
        if lang == "ru"
        else "Shahar nomini yozing, ob-havo ma’lumotini olish uchun 🌤"
    )

    await callback.message.answer(text)
