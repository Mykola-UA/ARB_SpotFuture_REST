import json
import os
from datetime import datetime, timedelta

SUBSCRIPTIONS_FILE = "subscriptions.json"

def load_subscriptions():
    if os.path.exists(SUBSCRIPTIONS_FILE):
        with open(SUBSCRIPTIONS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_subscriptions(subs):
    with open(SUBSCRIPTIONS_FILE, "w") as f:
        json.dump(subs, f, indent=2)

def set_paid(user_id, days):
    """
    Активує/продовжує підписку на N днів для user_id.
    Якщо вже є підписка — додає дні до поточного paid_until.
    """
    user_id = str(user_id)
    subs = load_subscriptions()
    now = datetime.utcnow()
    if user_id in subs and "paid_until" in subs[user_id]:
        paid_until = datetime.fromisoformat(subs[user_id]["paid_until"])
        if paid_until > now:
            new_paid_until = paid_until + timedelta(days=int(days))
        else:
            new_paid_until = now + timedelta(days=int(days))
    else:
        new_paid_until = now + timedelta(days=int(days))
    subs[user_id] = {
        "paid_until": new_paid_until.isoformat()
    }
    save_subscriptions(subs)

def is_paid(user_id):
    """
    Перевіряє, чи підписка ще активна для user_id.
    """
    user_id = str(user_id)
    subs = load_subscriptions()
    now = datetime.utcnow()
    if user_id in subs and "paid_until" in subs[user_id]:
        paid_until = datetime.fromisoformat(subs[user_id]["paid_until"])
        return paid_until > now
    return False

def get_paid_until(user_id):
    user_id = str(user_id)
    subs = load_subscriptions()
    if user_id in subs and "paid_until" in subs[user_id]:
        return subs[user_id]["paid_until"]
    return None

def get_users():
    """
    Повертає всі chat_id (user_id) з підписок.
    """
    subs = load_subscriptions()
    return list(subs.keys())

def get_status(user_id):
    """
    Повертає текстовий статус підписки для user_id (для меню/status).
    """
    paid_until = get_paid_until(user_id)
    if paid_until:
        now = datetime.utcnow()
        until = datetime.fromisoformat(paid_until)
        days_left = (until - now).days
        if days_left > 0:
            return f"✅ Subscription active until {until.date()} ({days_left} day{'s' if days_left != 1 else ''})"
        else:
            return "❌ Subscription expired"
    return "❌ No subscription"

def get_all_subscriptions():
    """
    Повертає весь словник з підписками.
    """
    return load_subscriptions()
