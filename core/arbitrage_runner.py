import asyncio
import json
import os
from datetime import datetime, timezone, timedelta

from core.price_collector import fetch_live_prices, reset_bad_exchanges_log_daily
from core.arbitrage_engine import find_arbitrage_opportunities
from notify.telegram_notify import (
    format_arb_message, format_arb_message_blur,
    build_exchange_links, build_blur_exchange_links,
)
from config import is_admin, is_paid, get_users, MIN_PROFIT

SENT_SIGNALS_TIME_FILE = "sent_signals_time.json"
ANTI_DUPLICATE_MINUTES = 60  # не дублювати мінімум 60 хв

def make_signal_id(arb):
    # Тільки унікальна пара: symbol|buy_exchange|sell_exchange|type_buy|type_sell
    return f"{arb['symbol']}|{arb['buy_exchange']}|{arb['sell_exchange']}|{arb.get('type_buy','')}|{arb.get('type_sell','')}"

def load_sent_signals_time():
    try:
        with open(SENT_SIGNALS_TIME_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_sent_signals_time(data):
    with open(SENT_SIGNALS_TIME_FILE, "w") as f:
        json.dump(data, f)

_run_flag = True

def stop_arbitrage_loop():
    global _run_flag
    _run_flag = False

async def arbitrage_loop(app):
    global _run_flag
    _run_flag = True
    while _run_flag:
        reset_bad_exchanges_log_daily()

        sent_signals_time = load_sent_signals_time()
        now = datetime.now(timezone.utc)

        spot_data = fetch_live_prices()
        arbs = find_arbitrage_opportunities(spot_data)
        arbs_profitable = [arb for arb in arbs if arb["net_profit"] > MIN_PROFIT]
        users = get_users()

        for arb in arbs_profitable:
            signal_id = make_signal_id(arb)
            last_time_str = sent_signals_time.get(signal_id)
            skip = False
            if last_time_str:
                try:
                    last_time = datetime.fromisoformat(last_time_str)
                    if now - last_time < timedelta(minutes=ANTI_DUPLICATE_MINUTES):
                        skip = True
                except Exception:
                    pass
            if skip:
                continue  # Не дублювати сигнал!

            for chat_id in users:
                if is_admin(chat_id) or is_paid(chat_id):
                    msg = format_arb_message(arb)
                    markup = build_exchange_links(arb)
                else:
                    msg = format_arb_message_blur(arb)
                    markup = build_blur_exchange_links(arb)
                try:
                    await app.bot.send_message(
                        chat_id=int(chat_id),
                        text=msg, parse_mode="HTML", reply_markup=markup
                    )
                except Exception as e:
                    print(f"❌ Не вдалося надіслати {chat_id}: {e}")
            # Зберігаємо час відправки для цієї пари
            sent_signals_time[signal_id] = now.isoformat()

        save_sent_signals_time(sent_signals_time)
        await asyncio.sleep(60)
