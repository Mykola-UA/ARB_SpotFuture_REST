import os
import requests
import json

CRYPTO_PAY_API_TOKEN = os.getenv("CRYPTO_PAY_API_TOKEN")
CRYPTO_PAY_API_URL = "https://api.cryptobot.one/invoice/create"

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

def create_cryptopay_invoice(user_id, amount, asset="USDT", description=None, days=None):
    """
    Створення інвойсу через CryptoBot API.
    Повертає: (pay_url, invoice_id)
    """
    if not CRYPTO_PAY_API_TOKEN:
        raise Exception("CRYPTO_PAY_API_TOKEN not set in environment variables!")

    headers = {
        "Content-Type": "application/json",
        "Crypto-Pay-API-Token": CRYPTO_PAY_API_TOKEN
    }

    # Формуємо description для invoice (user_id + тариф/кількість днів)
    if not description:
        description = f"Subscription for {user_id}"
        if days:
            description += f" {days}d"

    payload = {
        "asset": asset,
        "amount": float(amount),
        "description": description,
        "hidden_message": "Thank you for your payment!",  # message shown after payment
        "expires_in": 1800  # інвойс активний 30 хвилин
    }

    try:
        resp = requests.post(CRYPTO_PAY_API_URL, json=payload, headers=headers, timeout=15)
        data = resp.json()
    except Exception as e:
        raise Exception(f"Failed to create invoice: {e}")

    # CryptoPay: {"ok":true,"result":{"invoice_id":...,"pay_url":"https://..."}}
    if not data.get("ok") or not data.get("result"):
        raise Exception(f"Failed to create invoice: {data}")

    invoice_id = str(data["result"]["invoice_id"])
    pay_url = data["result"]["pay_url"]

    # === Зберігаємо user_id <-> invoice_id для подальшої обробки у webhook ===
    invoices = load_invoices()
    invoices[invoice_id] = {
        "user_id": user_id,
        "amount": amount,
        "asset": asset,
        "description": description,
        "days": days or None,
        "status": "pending"
    }
    save_invoices(invoices)

    return pay_url, invoice_id

# =================== WEBHOOK HANDLER ===================

from fastapi import FastAPI, Request
from notify.subscriptions import set_paid
from config import DAYS

app = FastAPI()

@app.post("/cryptopay_webhook")
async def cryptopay_webhook(request: Request):
    payload = await request.json()
    event = payload.get("event")
    data = payload.get("payload", {})
    invoice = data.get("invoice", {})

    if event == "invoice_paid":
        invoice_id = str(invoice.get("invoice_id"))
        invoices = load_invoices()
        user_info = invoices.get(invoice_id)

        if not user_info:
            # Фолбек: зчитати user_id із description
            desc = invoice.get("description", "")
            user_id = None
            if desc.startswith("Subscription for "):
                user_id = desc.replace("Subscription for ", "").split(" ")[0]
                tariff_label = "sub_7"  # дефолт, якщо не вказано тариф
            else:
                return {"ok": False, "reason": "No user info in description"}
        else:
            user_id = user_info.get("user_id")
            tariff_label = None
            # days -> sub_1/sub_7/sub_30 для set_paid
            days_val = user_info.get("days")
            for k, v in DAYS.items():
                if v == int(days_val):
                    tariff_label = k
                    break
            if not tariff_label:
                tariff_label = "sub_7"

        # Активуємо підписку
        days = DAYS.get(tariff_label, 7)
        set_paid(user_id, days)

        # Позначаємо як paid
        if invoice_id in invoices:
            invoices[invoice_id]["status"] = "paid"
            save_invoices(invoices)

        print(f"✅ Subscription activated for user {user_id} ({days} days) by invoice {invoice_id}")
        return {"ok": True}

    return {"ok": True}
