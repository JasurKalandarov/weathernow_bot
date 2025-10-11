import json
from pathlib import Path

# 📁 Файл, где будут храниться все пользователи
DATA_FILE = Path("data/users.json")
DATA_FILE.parent.mkdir(exist_ok=True)
if not DATA_FILE.exists():
    DATA_FILE.write_text("{}")


# --- Загружаем сохранённые данные ---
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 🔧 Преобразуем ключи обратно в int
            for key in data:
                data[key] = {int(k): v for k, v in data[key].items()}
            return data
    except Exception:
        return {}


# --- Сохраняем текущие данные ---
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# --- Инициализация состояния ---
_data = load_data()

user_languages = _data.get("user_languages", {})
user_cities = _data.get("user_cities", {})
last_messages = _data.get("last_messages", {})
user_notifications = _data.get("user_notifications", {})


# --- Функция для сохранения всех изменений ---
def persist_state():
    save_data({
        "user_languages": {str(k): v for k, v in user_languages.items()},
        "user_cities": {str(k): v for k, v in user_cities.items()},
        "last_messages": {str(k): v for k, v in last_messages.items()},
        "user_notifications": {str(k): v for k, v in user_notifications.items()}
    })
