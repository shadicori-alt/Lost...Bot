# connectors/facebook_connector.py
import os
import requests
from config import FB_PAGE_ACCESS_TOKEN

GRAPH_API = "https://graph.facebook.com/v14.0"

def post_comment(post_id, message):
    url = f"{GRAPH_API}/{post_id}/comments"
    params = {"message": message, "access_token": FB_PAGE_ACCESS_TOKEN}
    resp = requests.post(url, params=params, timeout=10)
    return resp.json()

def send_page_private_message(psid, message):
    url = f"{GRAPH_API}/me/messages"
    payload = {"recipient": {"id": psid}, "message": {"text": message}}
    resp = requests.post(url, params={"access_token": FB_PAGE_ACCESS_TOKEN}, json=payload, timeout=10)
    return resp.json()
