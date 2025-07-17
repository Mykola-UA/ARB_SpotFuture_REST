import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

from core.price_collector import fetch_live_prices
from core.arbitrage_engine import find_arbitrage_opportunities
from notify.telegram_notify import format_arb_message

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_CHAT_IDS = [x.strip() for x in os.getenv("ALLOWED_CHAT_IDS", "").split(",") if x.strip().isdigit()]

bot_running = False
background_task = None

def is_authorized(update: Update) -> bool:
    return str(update.effective_chat.id) in ALLOWED_CHAT_IDS

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_running, background_task

    if not is_authorized(update):
        await update.message.reply_text("⛔ Доступ заборонено.")
        return

    if bot_running:
        await update.message.reply_text("✅ Бот вже працює.")
        return

    await update.message.reply_text("🤖 Бот запущено!")
    bot_running = True

    background_task = asyncio.create_task(run_bot_loop(context.bot, update.effective_chat.id))

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_running, background_task

    if not is_authorized(update):
        await update.message.reply_text("⛔ Доступ заборонено.")
        return

    bot_running = False
    if background_task:
        background_task.cancel()
        background_task = None
    await update.message.reply_text("🛑 Бот зупинено.")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ Доступ заборонено.")
        return

    spot_data = fetch_live_prices()
    watchlist = {row["symbol"] for row in spot_data}
    filtered = [row for row in spot_data if row["symbol"] in watchlist]
    arbs = find_arbitrage_opportunities(filtered)
    arbs = [a for a in arbs if a["net_profit"] > 2]

    if not arbs:
        await update.message.reply_text("ℹ️ Немає прибуткових ситуацій.")
        return

    for arb in arbs[:10]:
        msg = format_arb_message(arb)
        await update.message.reply_text(msg, parse_mode="HTML")

async def run_bot_loop(bot, chat_id):
    global bot_running
    while bot_running:
        print("🟡 Telegram loop: збір цін...")
        spot_data = fetch_live_prices()
        watchlist = {row["symbol"] for row in spot_data}
        filtered = [row for row in spot_data if row["symbol"] in watchlist]
        arbs = find_arbitrage_opportunities(filtered)
        arbs = [a for a in arbs if a["net_profit"] > 2]

        for arb in arbs[:5]:
            msg = format_arb_message(arb)
            try:
                await bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")
            except Exception as e:
                print(f"❗️ Не вдалося надіслати повідомлення: {e}")

        await asyncio.sleep(60)

def run_telegram_controller():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stop", stop_command))
    app.add_handler(CommandHandler("status", status_command))
    print("🤖 Telegram-контролер запущено.")
    app.run_polling()

if __name__ == "__main__":
    run_telegram_controller()
