from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def language_keyboard():
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        types.InlineKeyboardButton(text="🇺🇿 O‘zbekcha", callback_data="lang_uz"),
    )
    return kb.as_markup()
