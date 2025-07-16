from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.cryptopay_api import create_cryptopay_invoice
from utils.webhook import load_invoices, save_invoices
from config import TARIFFS
from notify.subscriptions import is_paid, get_days_left

# --- Меню користувача: /start, /help, будь-яке текстове повідомлення
async def user_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    active = is_paid(user_id)
    left = get_days_left(user_id)
    status_text = (
        f"✅ Підписка активна ({left:.1f} днів)" if active
        else "❌ Підписка неактивна. Купіть доступ для сигналів!"
    )

    keyboard = [
        [InlineKeyboardButton("💸 Оплата USDT", callback_data="pay_usdt")],
        [InlineKeyboardButton("Перевірити статус", callback_data="check_status")]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👤 <b>Головне меню користувача</b>\n\n"
        f"{status_text}\n\n"
        "Оберіть дію нижче:",
        reply_markup=markup,
        parse_mode="HTML"
    )

# --- Callback'и (обробка кнопок)
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    if data == "pay_usdt":
        # Вибір тарифу (для простоти - тільки sub_7)
        sub_type = "sub_7"
        price = TARIFFS[sub_type]
        pay_url, invoice_id = create_cryptopay_invoice(
            user_id, price, asset="USDT", description=f"Subscription for {user_id} {sub_type}"
        )
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
    elif data == "check_status":
        active = is_paid(user_id)
        left = get_days_left(user_id)
        if active:
            msg = f"✅ Ваша підписка активна!\nЗалишилось днів: <b>{left:.1f}</b>"
        else:
            msg = "❌ У вас неактивна підписка."
        await query.answer()
        await query.message.reply_text(msg, parse_mode="HTML")
    elif data == "already_paid":
        await query.answer("Підписка активується автоматично після оплати, зазвичай протягом 1-2 хвилин.")
    else:
        await query.answer("Невідома дія.")

# --- Перевірити підписку через /check
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    active = is_paid(user_id)
    left = get_days_left(user_id)
    if active:
        msg = f"✅ Ваша підписка активна!\nЗалишилось днів: <b>{left:.1f}</b>"
    else:
        msg = "❌ У вас неактивна підписка."
    await update.message.reply_text(msg, parse_mode="HTML")

# --- Адмін-команди (заглушки, якщо потрібно - допиши логіку)
async def startbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущено (заглушка).")

async def stopbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот зупинено (заглушка).")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Статус бота: активний (заглушка).")

async def badex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("BadEx команда (заглушка).")

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот перезапущено (заглушка).")
