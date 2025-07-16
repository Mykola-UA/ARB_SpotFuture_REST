import os
import requests

CRYPTOPAY_API_TOKEN = os.getenv("CRYPTO_PAY_API_TOKEN")
CRYPTOPAY_API_URL = "https://api.cryptopay.me/v1/invoices"


def create_cryptopay_invoice(user_id, amount, asset="USDT", description=None):
    """
    Створює інвойс для оплати через CryptoBot та повертає pay_url і invoice_id.
    :param user_id: int або str — ID користувача Telegram (для ідентифікації)
    :param amount: float або int — сума оплати у валюті asset
    :param asset: str — токен оплати (USDT, TON, BTC, ETH, і т.д.)
    :param description: str — текст для description інвойсу (відображається у @CryptoBot)
    :return: (pay_url, invoice_id)
    """
    if not CRYPTOPAY_API_TOKEN:
        raise RuntimeError("Не задано CRYPTO_PAY_API_TOKEN у змінних оточення!")

    headers = {"Crypto-Pay-API-Token": CRYPTOPAY_API_TOKEN}
    data = {
        "asset": asset,
        "amount": str(amount),
        "description": description or f"Subscription for {user_id}",
        "hidden_message": "Дякуємо за оплату! Поверніться у бот для активації підписки.",
        # Можна додати "payload": f"user_{user_id}", якщо хочеш відслідковувати user_id як payload
    }
    resp = requests.post(CRYPTOPAY_API_URL, json=data, headers=headers, timeout=20)
    resp.raise_for_status()
    jdata = resp.json()

    if not jdata.get("ok"):
        raise RuntimeError(f"CryptoPay API error: {jdata}")

    invoice = jdata["result"]
    pay_url = invoice["pay_url"]
    invoice_id = invoice["invoice_id"]
    return pay_url, invoice_id


# Опціонально: функція для перевірки статусу інвойсу (якщо треба вручну)
def check_invoice_status(invoice_id):
    """
    Перевіряє статус інвойсу через CryptoPay API.
    :param invoice_id: str
    :return: статус (наприклад, "active", "paid", "expired")
    """
    url = f"https://api.cryptopay.me/v1/invoices/{invoice_id}"
    headers = {"Crypto-Pay-API-Token": CRYPTOPAY_API_TOKEN}
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    jdata = resp.json()
    if not jdata.get("ok"):
        raise RuntimeError(f"CryptoPay API error: {jdata}")
    invoice = jdata["result"]
    return invoice["status"]
