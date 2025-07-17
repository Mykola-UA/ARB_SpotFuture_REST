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
    user_id = str(user_id)
    subs = load_subscriptions()
    now = datetime.utcnow()
    paid_until = now
    if user_id in subs and "paid_until" in subs[user_id]:
        try:
            old_paid_until = datetime.fromisoformat(subs[user_id]["paid_until"])
            if old_paid_until > now:
                paid_until = old_paid_until
        except Exception:
            pass
    new_paid_until = paid_until + timedelta(days=int(days))
    subs[user_id] = {
        "paid_until": new_paid_until.isoformat()
    }
    save_subscriptions(subs)

def is_paid(user_id):
    user_id = str(user_id)
    subs = load_subscriptions()
    now = datetime.utcnow()
    try:
        paid_until = datetime.fromisoformat(subs[user_id]["paid_until"])
        return paid_until > now
    except Exception:
        return False

def get_paid_until(user_id):
    user_id = str(user_id)
    subs = load_subscriptions()
    return subs.get(user_id, {}).get("paid_until")

def get_users():
    subs = load_subscriptions()
    return list(subs.keys())

def get_status(user_id):
    paid_until = get_paid_until(user_id)
    if paid_until:
        now = datetime.utcnow()
        try:
            until = datetime.fromisoformat(paid_until)
            seconds_left = (until - now).total_seconds()
            days_left = int(seconds_left // (24 * 3600))
            hours_left = int((seconds_left % (24 * 3600)) // 3600)
            if seconds_left > 0:
                return f"✅ Subscription active until {until.date()} ({days_left} days, {hours_left} hours left)"
            else:
                return "❌ Subscription expired"
        except Exception:
            return "❌ Subscription expired"
    return "❌ No subscription"

def get_all_subscriptions():
    return load_subscriptions()
