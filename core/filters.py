# Модуль для кастомних фільтрів (whitelist, blacklist, special logic)
import pandas as pd

def filter_whitelist(df, whitelist):
    return df[df["symbol"].isin(whitelist)]

def filter_blacklist(df, blacklist):
    return df[~df["symbol"].isin(blacklist)]

def remove_suspicious_price_diff(df, max_diff_percent=5):
    stats = df.groupby("symbol")["price"].agg(["min", "max"])
    stats["diff_percent"] = (stats["max"] - stats["min"]) / stats["min"] * 100
    suspicious = stats[stats["diff_percent"] > max_diff_percent].index.tolist()
    clean_df = df[~df["symbol"].isin(suspicious)]
    return clean_df
