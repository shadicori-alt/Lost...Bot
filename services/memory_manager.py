# services/memory_manager.py
import json
import logging
from datetime import datetime
from models import SessionLocal, Memory
from services.ai_knowledge import add_kb_article

logger = logging.getLogger(__name__)

def save_memory(sender: str, role: str, message: str, reply: str = None):
    """يحفظ كل تفاعل في الذاكرة (db)"""
    db = SessionLocal()
    try:
        mem = Memory(
            sender=sender,
            role=role,
            message=message,
            reply=reply,
            timestamp=datetime.utcnow()
        )
        db.add(mem)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.exception("Memory save failed: %s", e)
        return False
    finally:
        db.close()

def get_recent_memory(sender: str, limit: int = 10):
    """يحصل على آخر تفاعلات لشخص معين"""
    db = SessionLocal()
    try:
        rows = (
            db.query(Memory)
            .filter(Memory.sender == sender)
            .order_by(Memory.timestamp.desc())
            .limit(limit)
            .all()
        )
        return [{"msg": r.message, "reply": r.reply, "ts": r.timestamp} for r in rows]
    finally:
        db.close()

def auto_learn_from_message(sender: str, message: str, reply: str = ""):
    """يحاول استنتاج معلومة جديدة من الرسائل"""
    lower = message.lower()
    keywords = ["يعالج", "يفيد", "مفيد", "يستخدم", "يقلل", "يحسن"]
    if any(k in lower for k in keywords) and len(message.split()) > 5:
        # إذا فيه معلومة طبية أو وصفية.. خزّنها في KB
        add_kb_article(title=message[:100], content=message, source="auto_chat", tags="auto")
        logger.info("Auto-learned from chat: %s", message)
        return True
    return False
