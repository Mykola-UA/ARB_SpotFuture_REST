import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
from utils.cryptopay_api import create_cryptopay_invoice
from utils.webhook import load_invoices, save_invoices
from config import TARIFFS

# /start — головне меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    keyboard = [
        [InlineKeyboardButton("💸 Оплата USDT", callback_data="pay_usdt")],
        [InlineKeyboardButton("💳 Купити USDT карткою", callback_data="buy_usdt_card")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Вітаємо!\n\n"
        "Щоб отримати доступ до сигналів, оберіть спосіб оплати:",
        reply_markup=markup
    )

# Обробка callback кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data == "pay_usdt":
        await pay_usdt_handler(query, context)
    elif data == "buy_usdt_card":
        await buy_usdt_card_handler(query, context)
    elif data == "already_paid":
        await query.answer("Після оплати інвойсу підписка активується автоматично. Зазвичай це займає 1-2 хвилини.")
    else:
        await query.answer("Невідома дія.")

# Створення інвойсу CryptoPay та кнопки для оплати USDT
async def pay_usdt_handler(query, context):
    user_id = query.from_user.id
    sub_type = "sub_7"         # Можна додати вибір тарифу
    price = TARIFFS[sub_type]

    # Створити invoice через CryptoPay
    pay_url, invoice_id = create_cryptopay_invoice(
        user_id, price, asset="USDT", description=f"Subscription for {user_id} {sub_type}"
    )

    # Зберігаємо invoice_id ↔ user_id + tariff
    invoices_map = load_invoices()
    invoices_map[invoice_id] = {
        "user_id": user_id,
        "tariff": sub_type
    }
    save_invoices(invoices_map)

    keyboard = [
        [InlineKeyboardButton("💸 Оплатити через CryptoBot", url=pay_url)],
        [InlineKeyboardButton("Вже оплатив", callback_data="already_paid")]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        "1️⃣ Натисніть <b>«Оплатити через CryptoBot»</b> (відкриється @CryptoBot)\n"
        "2️⃣ Проведіть оплату USDT\n"
        "3️⃣ Поверніться у цей бот — підписка активується автоматично!\n\n"
        "<i>Якщо вже оплатили — натисніть кнопку «Вже оплатив».</i>",
        parse_mode="HTML",
        reply_markup=markup
    )
    await query.answer()

# Інструкція для тих, хто хоче купити USDT карткою
async def buy_usdt_card_handler(query, context):
    await query.message.reply_text(
        "💳 Щоб оплатити карткою:\n"
        "1. Придбайте USDT через будь-яку біржу або сервіс (наприклад, Binance P2P, WhiteBIT, Kuna, BestChange).\n"
        "2. Поверніться до цього бота й оплатіть через кнопку «Оплата USDT»."
    )
    await query.answer()

# (Додай інші хендлери, якщо потрібно)

# === Ініціалізація бота (тільки приклад) ===
def main():
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    # Додай інші хендлери

    app.run_polling()

if __name__ == "__main__":
    main()
