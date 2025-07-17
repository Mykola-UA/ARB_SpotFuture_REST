import os
from datetime import datetime, timezone
import traceback

from exchanges.binance import fetch_binance_prices
from exchanges.bybit import fetch_bybit_prices
from exchanges.kucoin import fetch_kucoin_prices
from exchanges.mexc import fetch_mexc_prices
from exchanges.bitget import fetch_bitget_prices
from exchanges.bitmart import fetch_bitmart_prices
from exchanges.htx import fetch_htx_prices
from exchanges.gate import fetch_gate_prices
from exchanges.coinex import fetch_coinex_prices
from exchanges.bingx import fetch_bingx_prices
from exchanges.whitebit import fetch_whitebit_prices

EXCHANGES = [
    ("binance", fetch_binance_prices),
    ("bybit", fetch_bybit_prices),
    ("kucoin", fetch_kucoin_prices),
    ("mexc", fetch_mexc_prices),
    ("bitget", fetch_bitget_prices),
    ("bitmart", fetch_bitmart_prices),
    ("htx", fetch_htx_prices),
    ("gate", fetch_gate_prices),
    ("coinex", fetch_coinex_prices),
    ("bingx", fetch_bingx_prices),
    ("whitebit", fetch_whitebit_prices),
]

BAD_LOG_FILE = "bad_exchanges.log"
BAD_LOG_DATE_FILE = "bad_exchanges_date.txt"

def log_bad_exchange(exchange, reason, exception=None):
    dt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{dt} | {exchange}: {reason}"
    if exception:
        error_code = getattr(exception, "code", None)
        log_line += f" | Exception: {repr(exception)}"
        if error_code:
            log_line += f" | Error code: {error_code}"
        tb = traceback.format_exc()
        log_line += f"\nTraceback: {tb}"
    log_line += "\n"
    with open(BAD_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)

def fetch_live_prices():
    all_data = []
    for exchange_name, fetch_func in EXCHANGES:
        try:
            data = fetch_func()
            if not data or (isinstance(data, list) and len(data) == 0):
                log_bad_exchange(exchange_name, "No data returned from fetch_func()", exception="NO_DATA")
                print(f"❗️ {exchange_name}: No data [NO_DATA]")
                continue
            all_data.extend(data)
        except Exception as e:
            error_code = getattr(e, "code", None)
            error_msg = str(e)
            log_bad_exchange(exchange_name, "Exception during fetch", exception=e)
            if error_code:
                print(f"❗️ {exchange_name}: Error code {error_code} — {error_msg}")
            else:
                print(f"❗️ {exchange_name}: Error — {error_msg}")
    return all_data

def get_bad_exchanges(limit=10):
    if not os.path.exists(BAD_LOG_FILE):
        return []
    with open(BAD_LOG_FILE, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[-limit:]

def clear_bad_exchanges_log():
    open(BAD_LOG_FILE, "w").close()

def reset_bad_exchanges_log_daily():
    today = datetime.now(timezone.utc).date().isoformat()
    try:
        with open(BAD_LOG_DATE_FILE, "r") as f:
            last_date = f.read().strip()
    except Exception:
        last_date = ""
    if last_date != today:
        clear_bad_exchanges_log()
        with open(BAD_LOG_DATE_FILE, "w") as f:
            f.write(today)
