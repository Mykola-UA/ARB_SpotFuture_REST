import ccxt

def fetch_bitmart_prices():
        try:
            exchange = ccxt.bitmart()  # ім'я біржі
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
                        "exchange": "bitmart",  # наприклад, "Bybit"
                        "type": "spot"
                    })
            if not result:
                raise RuntimeError("No USDT tickers returned, API is up but empty data")
            return result
        except Exception as e:
            error_code = getattr(e, "code", None)
            msg = f"bitmart fetch failed: {e}"
            if error_code:
                msg += f" [Error code: {error_code}]"
            raise RuntimeError(msg)

