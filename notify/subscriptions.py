import json
import time

USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def set_paid(user_id, days):
    """
    Активує підписку для користувача на N днів з сьогоднішнього дня.
    """
    user_id = str(user_id)
    users = load_users()
    now = int(time.time())
    days_sec = days * 24 * 60 * 60
    paid_until = now + days_sec

    # Якщо підписка ще активна — продовжуємо її, а не перезаписуємо!
    if user_id in users and users[user_id].get("paid_until", 0) > now:
        paid_until = users[user_id]["paid_until"] + days_sec

    users[user_id] = {
        "paid": True,
        "paid_until": paid_until,
        "last_payment": now,
    }
    save_users(users)
    print(f"🔔 User {user_id} subscription set to {paid_until} ({days} днів)")

def is_paid(user_id):
    """
    Перевіряє, чи є активна підписка у користувача.
    """
    user_id = str(user_id)
    users = load_users()
    now = int(time.time())
    info = users.get(user_id)
    if not info:
        return False
    return info.get("paid", False) and info.get("paid_until", 0) > now

def get_paid_until(user_id):
    """
    Повертає timestamp закінчення підписки або None.
    """
    user_id = str(user_id)
    users = load_users()
    info = users.get(user_id)
    if not info:
        return None
    return info.get("paid_until")

def get_days_left(user_id):
    """
    Повертає кількість днів до кінця підписки (може бути float).
    """
    paid_until = get_paid_until(user_id)
    if not paid_until:
        return 0
    now = int(time.time())
    left = paid_until - now
    return max(left / (24 * 60 * 60), 0)

# (опціонально) Функція для адміністраторів — скинути підписку
def reset_subscription(user_id):
    users = load_users()
    if str(user_id) in users:
        del users[str(user_id)]
        save_users(users)
        print(f"🔔 User {user_id} subscription RESET")

