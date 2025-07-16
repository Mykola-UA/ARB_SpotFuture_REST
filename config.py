import os

# === ТАРИФИ І ПІДПИСКИ ===

# Тарифи: ключ -> ціна в USDT
TARIFFS = {
    "sub_1": 2,     # 2 USDT за 1 день
    "sub_7": 10,    # 10 USDT за 7 днів
    "sub_30": 30,   # 30 USDT за 30 днів
}

# Кількість днів для кожного тарифу
DAYS = {
    "sub_1": 1,
    "sub_7": 7,
    "sub_30": 30,
}

# === ОБМЕЖЕННЯ ТА ДОСТУП ===

# Мінімальний профіт для сигналу (%)
MIN_PROFIT = float(os.getenv("MIN_PROFIT", "1.0"))

# Дозволені користувачі (опціонально, через .env: ALLOWED_CHAT_IDS=12345,67890)
ALLOWED_CHAT_IDS = [
    int(chat_id) for chat_id in os.getenv("ALLOWED_CHAT_IDS", "").split(",") if chat_id
]

# Адміни (через .env: ADMIN_CHAT_IDS=12345,67890)
ADMIN_CHAT_IDS = [
    int(chat_id) for chat_id in os.getenv("ADMIN_CHAT_IDS", "").split(",") if chat_id
]

# === API-КЛЮЧІ БІРЖ ===

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

#BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
#BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")

BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET")
BITGET_API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")

GATE_API_KEY = os.getenv("GATE_API_KEY")
GATE_API_SECRET = os.getenv("GATE_API_SECRET")

MEXC_API_KEY = os.getenv("MEXC_API_KEY")
MEXC_API_SECRET = os.getenv("MEXC_API_SECRET")

HTX_API_KEY = os.getenv("HTX_API_KEY")
HTX_API_SECRET = os.getenv("HTX_API_SECRET")

#COINEX_API_KEY = os.getenv("COINEX_API_KEY")
#COINEX_API_SECRET = os.getenv("COINEX_API_SECRET")

BITMART_API_KEY = os.getenv("BITMART_API_KEY")
BITMART_API_SECRET = os.getenv("BITMART_API_SECRET")

OKX_API_KEY = os.getenv("OKX_API_KEY")
OKX_API_SECRET = os.getenv("OKX_API_SECRET")
OKX_API_PASSPHRASE = os.getenv("OKX_API_PASSPHRASE")

WHITEBIT_API_KEY = os.getenv("WHITEBIT_API_KEY")
WHITEBIT_API_SECRET = os.getenv("WHITEBIT_API_SECRET")

BINGX_API_KEY = os.getenv("BINGX_API_KEY")
BINGX_API_SECRET = os.getenv("BINGX_API_SECRET")

# === CryptoPay (для інвойсів через @CryptoBot) ===
CRYPTO_PAY_API_TOKEN = os.getenv("CRYPTO_PAY_API_TOKEN")

# === Telegram Bot Token ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# === Інші глобальні налаштування ===
# Додавай сюди за потреби
