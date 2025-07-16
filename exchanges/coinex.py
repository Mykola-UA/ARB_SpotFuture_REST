import ccxt

def fetch_coinex_prices():
    try:
        exchange = ccxt.coinex()
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
                    "exchange": "Coinex",
                    "type": "spot"
                })
        # Якщо немає даних по USDT — підняти виняток для логування
        if not result:
            raise RuntimeError("No USDT tickers returned, status code 200 but data empty")
        return result
    except Exception as e:
        # ccxt винятки іноді мають code (наприклад, e.code == 429 або 403)
        error_code = getattr(e, "code", None)
        msg = f"Coinex fetch failed: {e}"
        if error_code:
            msg += f" [Error code: {error_code}]"
        raise RuntimeError(msg)
