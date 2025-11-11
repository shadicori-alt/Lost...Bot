# services/notifier.py
from connectors.whatsapp_connector import send_whatsapp_text
from connectors.facebook_connector import send_page_private_message

def notify_agent_via_whatsapp(agent_phone, message):
    return send_whatsapp_text(agent_phone, message)

def notify_customer_facebook(psid, message):
    return send_page_private_message(psid, message)
