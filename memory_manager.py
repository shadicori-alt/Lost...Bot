import logging
from datetime import datetime
from models import SessionLocal, Memory
from services.ai_knowledge import add_kb_article

logger = logging.getLogger(__name__)

def save_memory(sender: str, role: str, message: str, reply: str = None):
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

def auto_learn_from_message(sender: str, message: str, reply: str = ""):
    lower = message.lower()
    keywords = ["يعالج", "يفيد", "مفيد", "يستخدم", "يقلل", "يحسن"]
    if any(k in lower for k in keywords) and len(message.split()) > 5:
        add_kb_article(title=message[:100], content=message, source="auto_chat", tags="auto")
        logger.info("Auto-learned from chat: %s", message)
        return True
    return False
