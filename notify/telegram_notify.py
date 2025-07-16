from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def blur(text):
    return ''.join('•' if c not in ['/', ' '] else c for c in str(text))

def exchange_icon(ex_type):
    if ex_type is None:
        return ""
    ex_type = str(ex_type).lower()
    if ex_type == "spot":
        return "🟢 spot"
    if ex_type == "futures":
        return "🔵 futures"
    return ""

def format_arb_message(arb):
    return (
        f"📈 <b>{arb['symbol']}</b>\n"
        f"🔻 <b>BUY:</b> {arb['buy_exchange']}  — ${arb['buy_price']} {exchange_icon(arb.get(' '))}\n"
        f"🔺 <b>SELL:</b> {arb['sell_exchange']} — ${arb['sell_price']} {exchange_icon(arb.get(' '))}\n"
        f"💰 {arb['net_profit']}% → ~{arb['usdt_profit']} USDT (100$)\n"
        f"📊 <b>Volume:</b> {arb['volume']} USDT"
    )

def format_arb_message_blur(arb):
    return (
        f"📈 <b>{blur(arb['symbol'])}</b>\n"
        f"🔻 <b>BUY:</b> {blur(arb['buy_exchange'])}  — ••••••\n"
        f"🔺 <b>SELL:</b> {blur(arb['sell_exchange'])} — ••••••\n"
        f"💰 {arb['net_profit']}% → ~{arb['usdt_profit']} USDT (100$)\n"
        f"📊 <b>Volume:</b> ••••• USDT\n"
        f"🔒 <i>Сигнали доступні лише з підпискою</i>"
    )

EXCHANGE_URLS = {
    "binance": "https://www.binance.com/en/trade/{symbol}",
    "gate": "https://www.gate.io/trade/{symbol}",
    "bitmart": "https://www.bitmart.com/trade/en?symbol={symbol}",
    "bybit": "https://www.bybit.com/en-US/trade/spot/{symbol}",
    "kucoin": "https://www.kucoin.com/trade/{symbol}",
    "mexc": "https://www.mexc.com/exchange/{symbol}",
    "htx": "https://www.htx.com/trade/{symbol}",
    "bitget": "https://www.bitget.com/spot/{symbol}",
    "coinex": "https://www.coinex.com/en/exchange/{symbol}",
    "bingx": "https://bingx.com/en/spot/{symbol}",
    "whitebit": "https://whitebit.com/trade/{symbol}"
}
EXCHANGE_PAIR_FORMATS = {
    "binance": "uscore",
    "gate": "uscore",
    "bitmart": "uscore",
    "bybit": "noslash",
    "kucoin": "dash",
    "mexc": "uscore",
    "htx": "uscore",
    "bitget": "noslash",
    "coinex": "dash",
    "bingx": "noslash",
    "whitebit": "uscore"
}

def get_pair_for_exchange(symbol, exchange):
    base, quote = symbol.upper().split("/")
    fmt = EXCHANGE_PAIR_FORMATS.get(exchange, "uscore")
    if fmt == "uscore":
        return f"{base}_{quote}"
    elif fmt == "dash":
        return f"{base}-{quote}"
    elif fmt == "noslash":
        return f"{base}{quote}"
    elif fmt == "lower":
        return f"{base.lower()}{quote.lower()}"
    elif fmt == "slash":
        return f"{base}/{quote}"
    else:
        return f"{base}_{quote}"

def build_exchange_links(arb):
    buy_exchange = arb["buy_exchange"].lower()
    sell_exchange = arb["sell_exchange"].lower()
    pair_buy = get_pair_for_exchange(arb["symbol"], buy_exchange)
    pair_sell = get_pair_for_exchange(arb["symbol"], sell_exchange)
    url_buy = EXCHANGE_URLS.get(buy_exchange)
    url_sell = EXCHANGE_URLS.get(sell_exchange)
    buttons = []
    if url_buy:
        url_buy = url_buy.replace("{symbol}", pair_buy)
        buttons.append(InlineKeyboardButton(f"🔻 BUY {arb['buy_exchange']}", url=url_buy))
    if url_sell:
        url_sell = url_sell.replace("{symbol}", pair_sell)
        buttons.append(InlineKeyboardButton(f"🔺 SELL {arb['sell_exchange']}", url=url_sell))
    if buttons:
        return InlineKeyboardMarkup([buttons])
    return None

def build_blur_exchange_links(arb):
    buttons = [
        InlineKeyboardButton(f"🔻 Купити на {blur(arb['buy_exchange'])}", url=""),  # прибрав посилання на your_bot
        InlineKeyboardButton(f"🔺 Продати на {blur(arb['sell_exchange'])}", url="")
    ]
    return InlineKeyboardMarkup([buttons])
