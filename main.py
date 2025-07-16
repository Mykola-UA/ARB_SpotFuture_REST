import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

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

# Завантаження токену з .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def main():
    # Створення Telegram Application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # 📩 Команди для всіх користувачів
    app.add_handler(CommandHandler("start", user_menu))
    app.add_handler(CommandHandler("help", user_menu))
    app.add_handler(CommandHandler("check", check))

    # ⚙️ Команди для адміністратора
    app.add_handler(CommandHandler("startbot", startbot))
    app.add_handler(CommandHandler("stopbot", stopbot))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("badex", badex))
    app.add_handler(CommandHandler("restart", restart))

    # 🔘 Callback кнопки та звичайні повідомлення
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), user_menu))

    print("🤖 Bot is waiting for Telegram commands...")
    app.run_polling()


if __name__ == "__main__":
    main()
