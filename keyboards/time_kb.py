from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def time_keyboard():
    kb = InlineKeyboardBuilder()

    for hour in range(0, 24):
        time_text = f"{hour:02d}:00"
        kb.add(types.InlineKeyboardButton(text=time_text, callback_data=f"set_time_{hour:02d}"))

    kb.adjust(6)
    return kb.as_markup()
