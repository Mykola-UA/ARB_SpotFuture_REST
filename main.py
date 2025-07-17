import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    PreCheckoutQueryHandler,
)
from telegram import Update

from bot.handlers import (
    user_menu,
    handle_callback,
    check,
    startbot,
    stopbot,
    status,
    badex,
    restart
)
from notify.subscriptions import set_paid, DAYS

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def precheckout_callback(update: Update, context):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment_handler(update: Update, context):
    user_id = update.effective_user.id
    payload = update.message.successful_payment.invoice_payload
    try:
        parts = payload.split("_")
        if len(parts) >= 3 and parts[0] == "sub":
            days_label = parts[1]  # "1", "7", "30"
            days = DAYS.get(f"sub_{days_label}", 7)
            set_paid(user_id, days)
            await update.message.reply_text("✅ Subscription activated via Stars! Дякуємо за оплату.")
        else:
            await update.message.reply_text("Unknown payment payload. Please contact admin.")
    except Exception as e:
        await update.message.reply_text("❌ Error processing payment. Please contact support.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Команди
    app.add_handler(CommandHandler("start", user_menu))
    app.add_handler(CommandHandler("help", user_menu))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("startbot", startbot))
    app.add_handler(CommandHandler("stopbot", stopbot))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("badex", badex))
    app.add_handler(CommandHandler("restart", restart))

    # Callback-и і звичайні повідомлення
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), user_menu))

    # Оплата
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_handler))

    print("🤖 Bot is waiting for Telegram commands...")
    app.run_polling()

if __name__ == "__main__":
    main()
