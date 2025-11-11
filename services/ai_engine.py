# services/ai_engine.py
import os, json
from openai import OpenAI
from models.models import KBArticle, Product, SessionLocal
from datetime import datetime

class AiEngine:
    def __init__(self):
        key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=key) if key else None

    def parse_intent(self, text):
        # Use a light prompt to classify intent and extract entities
        prompt = f"Classify the intent of this message and extract key entities as JSON.\n\nMessage: '''{text}'''"
        if not self.client:
            return 'unknown', {}
        resp = self.client.chat.completions.create(model="gpt-4", messages=[{"role":"user","content":prompt}], max_tokens=200)
        try:
            out = resp.choices[0].message.content
            # expect JSON; fallback naive parse
            parsed = json.loads(out)
            return parsed.get('intent','unknown'), parsed.get('entities',{})
        except Exception:
            return 'unknown', {}

    def generate_reply(self, user_text, tone='formal_friendly', context=None):
        # Search KB for relevant articles & products
        db = SessionLocal()
        results = db.query(KBArticle).filter(KBArticle.content.ilike(f"%{user_text[:40]}%")).limit(5).all()
        kb_snippets = "\n".join([f"- {r.title}: {r.content[:200]}" for r in results])
        db.close()

        prompt = f"You are a customer support assistant. Respond in a {tone} tone. Use the KB snippets if helpful.\n\nKB:\n{kb_snippets}\n\nCustomer: {user_text}\n\nReply:"
        if not self.client:
            return "الخدمة غير مفعّلة (OpenAI API key مفقود)."
        resp = self.client.chat.completions.create(model="gpt-4", messages=[{"role":"user","content":prompt}], max_tokens=400)
        return resp.choices[0].message.content
