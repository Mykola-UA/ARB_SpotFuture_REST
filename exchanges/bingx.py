import ccxt

def fetch_bingx_prices():
    try:
        exchange = ccxt.bingx()
        markets = exchange.fetch_tickers()
        result = []
        for symbol, data in markets.items():
            if not symbol.endswith("/USDT"):
                continue
            price = data.get("last") or data.get("close")
            volume = data.get("quoteVolume") or 0
            if price and volume:
                result.append({
                    "symbol": symbol,
                    "price": float(price),
                    "volume": float(volume),
                    "exchange": "Bingx",
                    "type": "spot"
                })
        # Якщо біржа вернула порожній результат:
        if not result:
            raise RuntimeError("No USDT tickers returned, status code 200 but data empty")
        return result
    except Exception as e:
        # Віддавай далі Exception для логування
        raise RuntimeError(f"Bingx fetch failed: {e}")
