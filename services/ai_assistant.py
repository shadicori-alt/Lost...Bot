# services/ai_assistant.py
from connectors.ai_connector import AIConnector
from models import SessionLocal, KBArticle, Order
from jinja2 import Template

ai = AIConnector()

def generate_reply_for_text(text, tone="formal_friendly", context=None):
    # Search KB articles simple full-text
    db = SessionLocal()
    try:
        articles = db.query(KBArticle).filter(KBArticle.content.ilike(f"%{text[:40]}%")).limit(5).all()
        snippets = "\n".join([a.content[:300] for a in articles])
    finally:
        db.close()
    prompt = f"""You are a helpful customer support assistant that replies in a {tone} tone.
Use the KB knowledge below when helpful.

KB:
{snippets}

Customer: {text}

Reply:"""
    return ai.simple_chat(prompt)
