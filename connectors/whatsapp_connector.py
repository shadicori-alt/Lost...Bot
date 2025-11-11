# connectors/whatsapp_connector.py
import os
import requests
from config import WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_ACCESS_TOKEN

GRAPH_API = "https://graph.facebook.com/v15.0"

def send_whatsapp_text(phone, text):
    url = f"{GRAPH_API}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "text": {"body": text}
    }
    headers = {"Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}", "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json=payload, timeout=10)
    return r.json()
