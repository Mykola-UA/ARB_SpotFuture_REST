import ccxt

# ✅ Спотові біржі
def get_spot_exchanges():
    return {
        'binance': ccxt.binance(),
        'kucoin': ccxt.kucoin(),
        'gate': ccxt.gateio(),
        'bybit': ccxt.bybit(),
        'bingx': ccxt.bingx(),
        'bitmart': ccxt.bitmart(),
        'coinex': ccxt.coinex(),
        'mexc': ccxt.mexc(),
        'htx': ccxt.huobi(),
        'bitget': ccxt.bitget(),
        'okx': ccxt.okx(),
        'whitebit': ccxt.whitebit()
    }

# ✅ Ф’ючерсні біржі
def get_futures_exchanges():
    return {
        'binance': ccxt.binance({'options': {'defaultType': 'future'}}),
        'kucoin': ccxt.kucoin({'options': {'defaultType': 'future'}}),
        'gate': ccxt.gateio({'options': {'defaultType': 'future'}}),
        'bybit': ccxt.bybit({'options': {'defaultType': 'future'}}),
        'bingx': ccxt.bingx({'options': {'defaultType': 'swap'}}),
        'bitget': ccxt.bitget({'options': {'defaultType': 'swap'}}),
        'okx': ccxt.okx({'options': {'defaultType': 'swap'}}),
        'htx': ccxt.huobi({'options': {'defaultType': 'swap'}}),
        # ⚠️ Додай інші лише якщо вони точно підтримують futures у ccxt
    }
