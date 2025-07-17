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

MIN_PROFIT = float(os.getenv("MIN_PROFIT", "3"))

def is_admin(chat_id):
    return int(chat_id) in ADMIN_CHAT_IDS
