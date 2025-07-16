mport asyncio
import os
import sys
import time
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from config import (
    USDT_PRICE, DAYS,
    is_admin, is_paid, set_paid, get_status, get_users
)
from core.price_collector import get_bad_exchanges
from core.arbitrage_runner import arbitrage_loop, stop_arbitrage_loop
from utils.cryptopay_api import create_cryptopay_invoice

arbitrage_task = None

async def user_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if is_admin(user_id):
        await update.message.reply_text(
            "👮 Admin Menu:\n"
            "/startbot - Start Arbitrage\n"
            "/stopbot - Stop Arbitrage\n"
            "/status - Check Bot Status\n"
            "/badex - Show Bad Exchanges\n"
            "/restart - Restart Bot"
        )
    else:
        keyboard = [
            [InlineKeyboardButton("▶️ START", callback_data="show_status")],
            [InlineKeyboardButton("💎 Subscribe", callback_data="subscribe")],
            [InlineKeyboardButton("❓ Help", callback_data="show_help")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Welcome! Subscribe to see signals from just 1 USDT.",
            reply_markup=markup
        )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.message.chat_id

    if data == "show_status":
        await query.edit_message_text(get_status(user_id))

    elif data == "subscribe":
        buttons = [
            [InlineKeyboardButton("1 USDT - 1 Day", callback_data="sub_1")],
            [InlineKeyboardButton("7 USDT - 7 Days", callback_data="sub_7")],
            [InlineKeyboardButton("30 USDT - 30 Days", callback_data="sub_30")],
        ]
        await query.edit_message_text(
            "Choose a subscription plan:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data in ("sub_1", "sub_7", "sub_30"):
        days = DAYS[data]
        price = USDT_PRICE[data]
        buttons = [
            [InlineKeyboardButton("💸 Pay USDT via CryptoBot", callback_data=f"{data}_CRYPTOPAY")],
            [InlineKeyboardButton("💳 Buy USDT with Card (CryptoBot)", url="https://t.me/CryptoBot?start=buy")]
        ]
        await query.edit_message_text(
            f"<b>Choose how to pay for your subscription ({price} USDT for {days} day(s)):</b>\n\n"
            "<b>💸 Pay USDT via CryptoBot:</b>\n"
            "- Use your existing USDT in @CryptoBot wallet to pay instantly and securely.\n\n"
            "<b>💳 Buy USDT with Card (CryptoBot):</b>\n"
            "- If you don’t have USDT, you can buy crypto directly in Telegram using your card (Visa/Mastercard, Apple Pay, Google Pay).\n"
            "- After purchase, come back here and use the first button to pay for your subscription.\n\n"
            "<i>Tip: USDT payment via CryptoBot is instant and with no extra fees.</i>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif any(data.startswith(sub) for sub in ("sub_1_", "sub_7_", "sub_30_")):
        sub_type, network = data.rsplit("_", 1)
        price = USDT_PRICE[sub_type]
        days = DAYS[sub_type]
        if network.upper() == "CRYPTOPAY":
            try:
                pay_url, invoice_id = create_cryptopay_invoice(user_id, price, asset="USDT")
                await query.edit_message_text(
                    f"To activate your <b>{days} day(s)</b> subscription:\n"
                    f"Pay <b>{price} USDT</b> via <b>CryptoBot</b> using the link below:\n\n"
                    f"<a href='{pay_url}'>💸 Click here to pay USDT via CryptoBot</a>\n\n"
                    "<i>Your subscription will be activated automatically after payment!</i>",
                    parse_mode="HTML"
                )
            except Exception as e:
                await query.edit_message_text(
                    f"Error creating invoice via CryptoBot:\n<code>{e}</code>",
                    parse_mode="HTML"
                )
        else:
            await query.edit_message_text("Unknown payment method.")

    elif data == "show_help":
        await query.edit_message_text(
            "This bot sends profitable arbitrage signals from top exchanges. Subscribe to unlock full access!"
        )
    else:
        await query.edit_message_text("Unknown action.")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please pay using the CryptoBot buttons in the menu. Your subscription is activated automatically after payment."
    )

# Admin commands
async def startbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global arbitrage_task
    if not is_admin(update.effective_chat.id):
        await update.message.reply_text("⛔ Admins only!")
        return
    if arbitrage_task and not arbitrage_task.done():
        await update.message.reply_text("✅ Already running.")
        return
    await update.message.reply_text("🟢 Started.")
    arbitrage_task = asyncio.create_task(arbitrage_loop(context.application))

async def stopbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global arbitrage_task
    if not is_admin(update.effective_chat.id):
        await update.message.reply_text("⛔ Admins only!")
        return
    if not arbitrage_task or arbitrage_task.done():
        await update.message.reply_text("❌ Not running.")
        return
    stop_arbitrage_loop()
    arbitrage_task.cancel()
    await update.message.reply_text("🛑 Stopped.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global arbitrage_task
    if not is_admin(update.effective_chat.id):
        await update.message.reply_text("⛔ Admins only!")
        return
    active = sum(1 for u in get_users().values() if is_paid(u))
    if arbitrage_task and not arbitrage_task.done():
        await update.message.reply_text(f"✅ Running.\nActive subscriptions: {active}")
    else:
        await update.message.reply_text(f"❌ Not running.\nActive subscriptions: {active}")

async def badex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_chat.id):
        await update.message.reply_text("⛔ Admins only!")
        return
    bad = get_bad_exchanges()
    if not bad:
        await update.message.reply_text("✅ All exchanges OK.")
    else:
        await update.message.reply_text("❗ Problem exchanges:\n" + "\n".join(bad))

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_chat.id):
        await update.message.reply_text("⛔ Admins only!")
        return
    await update.message.reply_text("🔄 Restarting...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

