from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def forecast_keyboard(lang: str = "ru"):
    kb = InlineKeyboardBuilder()
    if lang == "ru":
        kb.row(types.InlineKeyboardButton(text="🌤 Прогноз на сегодня", callback_data="forecast_today")),
        kb.row(types.InlineKeyboardButton(text="🌦 Прогноз на 3 дня", callback_data="forecast_3days")),
        kb.row(types.InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings"))
    else:
        kb.row(types.InlineKeyboardButton(text="🌤 Bugungi ob-havo", callback_data="forecast_today")),
        kb.row(types.InlineKeyboardButton(text="🌦 3 kunlik prognoz", callback_data="forecast_3days")),
        kb.row(types.InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings"))
    return kb.as_markup()
