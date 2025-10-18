from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from keyboards.language_kb import language_keyboard
from keyboards.forecast_kb import forecast_keyboard
from utils.state import user_languages, user_cities, persist_state

router = Router()


@router.message(F.text == "/start")
async def handle_start(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, есть ли сохранённый язык и город
    lang = user_languages.get(user_id)
    city = user_cities.get(user_id)

    if lang and city:
        question_text = (
            "Какой прогноз вы хотели бы получить?" if lang == "ru"
            else "Qaysi prognozni olishni xohlaysiz?"
        )
        await message.answer(
            f"👋 <b>С возвращением!</b>\n\n<b>{question_text}</b>",
            parse_mode="HTML",
            reply_markup=forecast_keyboard(lang)
        )
        return

    # Если язык ещё не выбран
    text = "Пожалуйста, выберите язык / Iltimos, tilni tanlang:"
    await message.answer(text, reply_markup=language_keyboard())

