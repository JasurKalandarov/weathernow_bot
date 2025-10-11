from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def notification_time_keyboard() -> types.InlineKeyboardMarkup:
    """Клавиатура для выбора времени рассылки (00:00 — 23:00), 6 кнопок в ряд"""
    kb = InlineKeyboardBuilder()

    buttons = [
        types.InlineKeyboardButton(text=f"{hour:02d}:00", callback_data=f"set_time_{hour}")
        for hour in range(24)
    ]

    # Добавляем кнопки по 6 штук в ряд
    for i in range(0, len(buttons), 6):
        kb.row(*buttons[i:i+6])

    # Кнопка "Назад"
    kb.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_settings"))

    return kb.as_markup()
