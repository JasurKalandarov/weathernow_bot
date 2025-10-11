from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from utils.state import last_messages


async def delete_previous(bot: Bot, chat_id: int, user_id: int):
    if user_id in last_messages:
        try:
            await bot.delete_message(chat_id, last_messages[user_id])
        except TelegramBadRequest:
            pass
        except Exception as e:
            print(f"⚠️ Ошибка при удалении сообщения: {e}")
