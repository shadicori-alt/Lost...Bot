# config.py
import os

# Load env variables (you can use python-dotenv in app to auto-load .env)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///lastbot.db')

# Facebook / Messenger
FB_PAGE_ACCESS_TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN', '')
FB_VERIFY_TOKEN = os.getenv('FB_VERIFY_TOKEN', '')
FB_APP_SECRET = os.getenv('FB_APP_SECRET', '')

# WhatsApp Cloud
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID', '')
WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN', '')

# OpenAI / DeepSeek
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_JSON = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON', '')  # path or JSON string
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '')

# App
SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-secret')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() in ('1','true','yes')

# Scheduler / polling
POLL_SECONDS = int(os.getenv('POLL_SECONDS', 5))
