# services/messenger_sender.py
import requests, os, json

FB_PAGE_TOKEN = os.getenv('FB_PAGE_TOKEN')
WHATSAPP_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')

def post_comment(page_id, post_id, message):
    url = f"https://graph.facebook.com/v14.0/{post_id}/comments"
    params = {'message': message, 'access_token': FB_PAGE_TOKEN}
    r = requests.post(url, params=params)
    return r.json()

def send_private_message(recipient_psid, message):
    url = f"https://graph.facebook.com/v14.0/me/messages"
    payload = {
        "recipient": {"id": recipient_psid},
        "message": {"text": message}
    }
    r = requests.post(url, params={'access_token': FB_PAGE_TOKEN}, json=payload)
    return r.json()

def send_whatsapp_message(phone_number, message):
    url = f"https://graph.facebook.com/v15.0/{os.getenv('WHATSAPP_PHONE_NUMBER_ID')}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "text": {"body": message}
    }
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type":"application/json"}
    r = requests.post(url, headers=headers, json=payload)
    return r.json()
