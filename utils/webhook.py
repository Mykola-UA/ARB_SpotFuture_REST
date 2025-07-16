from fastapi import FastAPI, Request
from notify.subscriptions import set_paid
from config import DAYS
import os

app = FastAPI()

# === Зберігаємо звʼязок invoice_id <-> user_id (тимчасово у файл, але бажано у БД/Redis) ===
import json
INVOICES_FILE = "invoices.json"

def load_invoices():
    try:
        with open(INVOICES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_invoices(data):
    with open(INVOICES_FILE, "w") as f:
        json.dump(data, f, indent=2)

# == Endpoint для Telegram CryptoBot (CryptoPayAPI) ==
@app.post("/cryptopay_webhook")
async def cryptopay_webhook(request: Request):
    payload = await request.json()

    # CryptoPay надсилає: event, payload: {invoice, ...}
    event = payload.get('event')
    data = payload.get('payload', {})
    invoice = data.get('invoice', {})

    # Тільки обробка оплаченого invoice
    if event == "invoice_paid":
        invoice_id = invoice.get("invoice_id")
        # Дістаємо user_id, тариф з description або через map invoice_id->user_id
        invoices_map = load_invoices()
        user_info = invoices_map.get(invoice_id)
        if not user_info:
            # Пробуємо зчитати user_id із description інвойсу
            desc = invoice.get("description", "")
            # description був: "Subscription for {user_id}"
            user_id = None
            if desc.startswith("Subscription for "):
                user_id = desc.replace("Subscription for ", "").strip()
                # Якщо треба тариф — зберігай у description, напр: "Subscription for {user_id} {tariff}"
                tariff_label = "sub_7"  # дефолт на 7 днів
            else:
                return {"ok": False, "reason": "No user info in description"}
        else:
            user_id = user_info.get("user_id")
            tariff_label = user_info.get("tariff", "sub_7")
        # Активуємо підписку
        days = DAYS.get(tariff_label, 7)
        set_paid(user_id, days)
        # (optionally) видаляємо invoice_id з invoices_map
        if invoice_id in invoices_map:
            del invoices_map[invoice_id]
            save_invoices(invoices_map)
        print(f"✅ Subscription activated for user {user_id} ({days} days) by invoice {invoice_id}")
        return {"ok": True}
    return {"ok": True}

