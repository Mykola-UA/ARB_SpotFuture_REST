import requests
import os

CRYPTO_PAY_API_TOKEN = os.getenv("CRYPTO_PAY_API_TOKEN")  # Додай у .env

def create_cryptopay_invoice(user_id, amount, asset="USDT"):
    """
    Створює інвойс на оплату через CryptoPay (Telegram @CryptoBot)
    """
    url = "https://api.cryptopay.me/v1/invoices"
    headers = {
        "Content-Type": "application/json",
        "Crypto-Pay-API-Token": CRYPTO_PAY_API_TOKEN
    }
    data = {
        "amount": float(amount),
        "asset": asset,
        "description": f"Subscription for {user_id}",
        "hidden_message": f"Дякуємо за оплату! Підписка буде активована автоматично."
    }
    resp = requests.post(url, json=data, headers=headers)
    r = resp.json()
    if r.get('ok'):
        return r['result']['pay_url'], r['result']['invoice_id']
    else:
        raise Exception(r.get('description', 'Unknown CryptoPay error'))
