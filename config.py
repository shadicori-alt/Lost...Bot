# config.py
import os

# ===== إعدادات عامة =====
APP_NAME = "LastBot Smart System"
APP_VERSION = "2.0"

# ===== إعدادات قاعدة البيانات =====
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///lastbot.db")

# ===== إعدادات فيسبوك =====
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
FACEBOOK_VERIFY_TOKEN = os.getenv("FACEBOOK_VERIFY_TOKEN", "")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET", "")

# ===== إعدادات واتساب =====
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "")

# ===== إعدادات الذكاء الصناعي =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# ===== إعدادات القوالب التلقائية =====
AUTO_REPLY_TEMPLATES = {
    "comment_thanks": {
        "template": "شكرًا لتعليقك، سنراسلك عبر الخاص للمتابعة. رقم الطلب: {{order_id}}",
        "assign_region": "القاهرة",
        "auto_create_order": True
    },
    "product_inquiry": {
        "template": "مرحبًا 👋، شكراً لسؤالك عن المنتج {{product_name}}. متاح حالياً! هل ترغب في إتمام الطلب؟",
        "assign_region": "الإسكندرية",
        "auto_create_order": True
    },
    "default_response": {
        "template": "شكرًا لتواصلك، فريق المبيعات سيرد عليك قريبًا ❤️",
        "assign_region": "عام",
        "auto_create_order": False
    }
}
