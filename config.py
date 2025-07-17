import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_IDS = set(int(x) for x in os.getenv("ADMIN_CHAT_IDS", "").split(",") if x.strip().isdigit())

CRYPTO_PAY_API_TOKEN = os.getenv("CRYPTO_PAY_API_TOKEN")

USDT_PRICE = {
    "sub_1": 1,
    "sub_7": 7,
    "sub_30": 30
}
DAYS = {
    "sub_1": 1,
    "sub_7": 7,
    "sub_30": 30
}

MIN_PROFIT = float(os.getenv("MIN_PROFIT", "3"))  # Відсоток мін. прибутку

def is_admin(chat_id):
    return int(chat_id) in ADMIN_CHAT_IDS

# ---- MOCK ФУНКЦІЇ ДЛЯ СУМІСНОСТІ (для початку роботи бота) ----

def is_paid(user_id):
    # TODO: заміни на справжню перевірку оплати/підписки
    return True

def get_users():
    # TODO: заміни на справжнє отримання користувачів
    return []

# Якщо get_status не в notify.subscriptions, можна додати:
def get_status(user_id):
    return "Ваша підписка активна!" if is_paid(user_id) else "Ваша підписка неактивна."

