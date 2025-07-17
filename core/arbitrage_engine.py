import pandas as pd
from datetime import datetime
from utils.fees import EXCHANGE_FEES

MIN_PRICE = 0.001
MAX_PRICE = 5.0
MIN_VOLUME = 10000
MIN_NET_PROFIT = 3.0
MAX_NET_PROFIT = 7.0  # ✅ не більше 7%

# Дозволені комбінації типів ринку: (buy_type, sell_type)
ALLOWED_TYPE_COMBOS = [
    ("spot", "spot"),
    ("spot", "futures"),
    ("futures", "spot"),
    ("futures", "futures")
]

def find_arbitrage_opportunities(spot_data):
    """
    Знаходить арбітражні можливості на основі даних з бірж.
    :param spot_data: список словників з полями symbol, price, volume, type, exchange
    :return: список арбітражних ситуацій
    """
    if not spot_data:
        return []

    df = pd.DataFrame(spot_data)

    # Фільтруємо за ціною та обсягом
    df = df[
        (df["price"] >= MIN_PRICE) &
        (df["price"] <= MAX_PRICE) &
        (df["volume"] >= MIN_VOLUME)
    ]

    df["symbol"] = df["symbol"].str.upper()
    df["type"] = df["type"].str.lower()
    grouped = df.groupby("symbol")

    results = []

    for symbol, group in grouped:
        for _, buy in group.iterrows():
            for _, sell in group.iterrows():
                if buy["exchange"] == sell["exchange"]:
                    continue
                if (buy["type"], sell["type"]) not in ALLOWED_TYPE_COMBOS:
                    continue

                buy_price = float(buy["price"])
                sell_price = float(sell["price"])
                volume = min(float(buy["volume"]), float(sell["volume"]))

                if sell_price <= buy_price or volume < MIN_VOLUME:
                    continue

                spread = ((sell_price - buy_price) / buy_price) * 100
                buy_fee = EXCHANGE_FEES.get(buy["exchange"], 0.1)
                sell_fee = EXCHANGE_FEES.get(sell["exchange"], 0.1)
                net_profit = spread - (buy_fee + sell_fee)

                # ✅ Фільтр 3% < net_profit < 7%
                if net_profit < MIN_NET_PROFIT or net_profit > MAX_NET_PROFIT:
                    continue

                results.append({
                    "symbol": symbol,
                    "buy_exchange": buy["exchange"].capitalize(),
                    "sell_exchange": sell["exchange"].capitalize(),
                    "type_buy": buy["type"],
                    "type_sell": sell["type"],
                    "buy_price": round(buy_price, 6),
                    "sell_price": round(sell_price, 6),
                    "price_diff": round(sell_price - buy_price, 6),
                    "spread": round(spread, 2),
                    "net_profit": round(net_profit, 2),
                    "usdt_profit": round((net_profit / 100) * 100, 2),  # на 100 USDT
                    "volume": round(volume, 2),
                    "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                })

    return results
