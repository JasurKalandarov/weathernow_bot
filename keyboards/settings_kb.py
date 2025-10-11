from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def settings_keyboard(lang: str = "ru", has_notifications: bool = False) -> types.InlineKeyboardMarkup:
    """Клавиатура для настроек (в зависимости от того, включена ли рассылка)"""
    kb = InlineKeyboardBuilder()

    if lang == "ru":
        kb.row(types.InlineKeyboardButton(text="🌐 Изменить язык", callback_data="change_lang"))
        kb.row(types.InlineKeyboardButton(text="🏙 Изменить город", callback_data="change_city"))

        if has_notifications:
            kb.row(types.InlineKeyboardButton(text="⏰ Изменить время рассылки", callback_data="change_time"))
            kb.row(types.InlineKeyboardButton(text="🔕 Отключить рассылку", callback_data="disable_notifications"))
        else:
            kb.row(types.InlineKeyboardButton(text="🔔 Включить рассылку", callback_data="enable_notifications"))

        kb.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_forecast"))

    else:
        kb.row(types.InlineKeyboardButton(text="🌐 Tilni o‘zgartirish", callback_data="change_lang"))
        kb.row(types.InlineKeyboardButton(text="🏙 Shaharni o‘zgartirish", callback_data="change_city"))

        if has_notifications:
            kb.row(types.InlineKeyboardButton(text="⏰ Xabarnoma vaqtini o‘zgartirish", callback_data="change_time"))
            kb.row(types.InlineKeyboardButton(text="🔕 Xabarnomani o‘chirish", callback_data="disable_notifications"))
        else:
            kb.row(types.InlineKeyboardButton(text="🔔 Xabarnomani yoqish", callback_data="enable_notifications"))

        kb.row(types.InlineKeyboardButton(text="⬅️ Orqaga qaytish", callback_data="back_to_forecast"))

    return kb.as_markup()
