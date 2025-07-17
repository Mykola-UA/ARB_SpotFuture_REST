import os
from dotenv import load_dotenv

load_dotenv()

# --- Telegram Bot Token ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- Admin Settings ---
ADMIN_IDS = os.getenv("ADMIN_CHAT_IDS", "")
ADMIN_CHAT_IDS = set(int(x) for x in ADMIN_IDS.split(",") if x.strip().isdigit())

def is_admin(chat_id):
    return int(chat_id) in ADMIN_CHAT_IDS

# --- Subscription/Payment Settings ---

# CryptoPay API Token (для оплати через @CryptoBot)
CRYPTO_PAY_API_TOKEN = os.getenv("CRYPTO_PAY_API_TOKEN")

# --- Tariffs ---
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

# --- Subscription Functions (підключення) ---
from notify.subscriptions import set_paid, is_paid, get_users

# --- Мінімальний % прибутку для сигналу ---
MIN_PROFIT = float(os.getenv("MIN_PROFIT", "3"))

# --- Language functions (залишено для локалізації, якщо треба) ---
def tr(key, lang="en", **kwargs):
    texts = dict(
        greet="Welcome! Subscribe to see signals for just 1 USDT.",
        status="Check your subscription status.",
        choose_network="Choose network:",
        address_text="Send <b>{price} USDT</b> via <b>{network}</b> to this address:\n<code>{address}</code>\n\nAfter payment send /check TX_HASH",
        help_text="This bot sends profitable arbitrage signals. Subscribe to unlock full access.",
    )
    text = texts.get(key, key)
    return text.format(**kwargs)

def get_lang(chat_id):
    return "en"

def set_lang(chat_id, lang):
    pass

def detect_lang(update):
    return "en"

# --- Шлях до файлу invoice mapping для webhook (CryptoPay) ---
INVOICES_FILE = os.getenv("INVOICES_FILE", "invoices.json")
