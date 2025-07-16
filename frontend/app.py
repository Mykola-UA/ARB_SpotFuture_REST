import streamlit as st
import pandas as pd
from core.price_collector import fetch_live_prices
from core.arbitrage_engine import find_arbitrage_opportunities

st.set_page_config(page_title="Live Arbitrage Scanner", layout="wide")
st.title("🟡 Live Arbitrage Scanner (Spot & Futures)")

if st.button("Оновити зараз"):
    spot_data = fetch_live_prices()
    arbs = find_arbitrage_opportunities(spot_data)
    if not arbs:
        st.warning("Валідних арбітражних ситуацій не знайдено.")
    else:
        df = pd.DataFrame(arbs)

        # Форматування колонок для виводу
        columns = [
            "symbol", "buy_exchange", "type_buy", "sell_exchange", "type_sell",
            "buy_price", "sell_price", "price_diff",
            "spread", "net_profit", "usdt_profit", "volume", "created_at"
        ]
        columns = [c for c in columns if c in df.columns]

        df_display = df[columns].copy()
        df_display = df_display.rename(columns={
            "symbol": "Пара",
            "buy_exchange": "Купити",
            "type_buy": "Тип купівлі",
            "sell_exchange": "Продати",
            "type_sell": "Тип продажу",
            "buy_price": "Ціна купівлі",
            "sell_price": "Ціна продажу",
            "price_diff": "Різниця",
            "spread": "Валовий спред (%)",
            "net_profit": "Чистий прибуток (%)",
            "usdt_profit": "USDT (на 100)",
            "volume": "Обʼєм",
            "created_at": "Час"
        })

        st.dataframe(df_display, use_container_width=True)
else:
    st.info("Натисни кнопку для сканування поточних ринків.")
