import json
from datetime import datetime, timezone, timedelta

USERS_FILE = "users.json"

def get_users():
    try:
        with open(USERS_FILE) as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def is_admin(chat_id, admin_list=None):
    # admin_list: список або set айдішників, передавати з config
    if admin_list:
        return str(chat_id) in admin_list or int(chat_id) in admin_list
    from config import ADMIN_CHAT_IDS
    return int(chat_id) in ADMIN_CHAT_IDS

def set_paid(chat_id, days):
    """
    Додає до існуючої підписки ще N днів (навіть якщо не закінчилась).
    Завжди округляє до 0:00 UTC.
    """
    users = get_users()
    now = datetime.now(timezone.utc)
    base_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    current = users.get(str(chat_id), {}).get("paid_until")
    if current:
        current_until = datetime.strptime(current, "%Y-%m-%d")
        if current_until > base_date:
            base_date = current_until
    paid_until = (base_date + timedelta(days=int(days))).strftime("%Y-%m-%d")
    users[str(chat_id)] = users.get(str(chat_id), {})
    users[str(chat_id)]["paid_until"] = paid_until
    save_users(users)

def is_paid(chat_id):
    users = get_users()
    info = users.get(str(chat_id), {})
    paid_until = info.get("paid_until")
    if paid_until:
        now = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        until = datetime.strptime(paid_until, "%Y-%m-%d")
        return until > now
    return False

def get_status(chat_id):
    users = get_users()
    info = users.get(str(chat_id), {})
    paid_until = info.get("paid_until")
    if paid_until:
        now = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        until = datetime.strptime(paid_until, "%Y-%m-%d")
        days = (until - now).days
        if days > 0:
            return f"✅ Active until {paid_until} ({days} day{'s' if days > 1 else ''})"
        else:
            return "❌ Subscription not active"
    return "❌ No subscription"

