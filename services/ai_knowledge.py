# services/ai_knowledge.py
# إدارة المكتبة المعرفية: مكتبة تسويقية للعملاء + مكتبة نظامية للمشكلات
import json
from pathlib import Path
from typing import List, Dict, Optional
from models import KBArticle, SessionLocal
import re
import logging

logger = logging.getLogger(__name__)

# Default data files (يمكن تعديل المسارات اذا رغبت)
MARKETING_KB = Path("data/knowledge_marketing.json")
SYSTEM_KB = Path("data/knowledge_system.json")

def load_local_files() -> List[Dict]:
    items = []
    for p in (MARKETING_KB, SYSTEM_KB):
        if p.exists():
            try:
                data = json.load(open(p, encoding="utf-8"))
                if isinstance(data, list):
                    items.extend(data)
            except Exception as e:
                logger.exception("Failed loading KB file %s: %s", p, e)
    return items

def seed_db_from_files():
    """يحمل محتوى ملفات JSON إلى جدول KBArticle إن لم تكن موجودة"""
    local = load_local_files()
    if not local:
        return {"status":"empty"}
    db = SessionLocal()
    try:
        for item in local:
            title = item.get("title")[:250]
            content = item.get("content","")
            source = item.get("source", "file")
            tags = item.get("tags", item.get("tags",""))
            # تفادي الازدواج: تحقق بعنصر مطابق بالعناوين
            exists = db.query(KBArticle).filter(KBArticle.title==title).first()
            if not exists:
                kb = KBArticle(title=title, content=content, source=source, tags=tags)
                db.add(kb)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.exception("Seeding KB failed: %s", e)
    finally:
        db.close()
    return {"status":"ok", "loaded": len(local)}

def search_kb(query: str, limit: int = 5) -> List[Dict]:
    """بحث بسيط: يبحث أولاً في DB ثم في الملفات كفشل"""
    q = query.lower().strip()
    db = SessionLocal()
    results = []
    try:
        # بحث نصي بسيط في الحقول title و content و tags
        rows = db.query(KBArticle).filter(
            (KBArticle.title.ilike(f"%{q}%")) |
            (KBArticle.content.ilike(f"%{q}%")) |
            (KBArticle.tags.ilike(f"%{q}%"))
        ).limit(limit).all()
        for r in rows:
            results.append({"title": r.title, "content": r.content, "source": r.source, "tags": r.tags})
    except Exception as e:
        logger.exception("DB search failed: %s", e)
    finally:
        db.close()

    # If no DB result, fallback to local files (best-effort)
    if not results:
        local = load_local_files()
        for item in local:
            txt = (item.get("title","")+" "+item.get("content","")).lower()
            if q in txt or any(tok in txt for tok in q.split()):
                results.append(item)
                if len(results) >= limit:
                    break
    return results

def add_kb_article(title: str, content: str, source: str="manual", tags: str=""):
    db = SessionLocal()
    try:
        kb = KBArticle(title=title[:300], content=content, source=source, tags=tags)
        db.add(kb)
        db.commit()
        return {"status":"ok","id":kb.id}
    except Exception as e:
        db.rollback()
        logger.exception("Add KB failed: %s", e)
        return {"status":"error", "error": str(e)}
    finally:
        db.close()

def best_kb_answer(query: str) -> Optional[str]:
    """تحاول إرجاع أنسب نص من المكتبة — إذا وجد"""
    hits = search_kb(query, limit=3)
    if not hits:
        return None
    # اختيار أفضل نتيجة بسيطة: الأفضل هو أول عنصر
    return hits[0]["content"]
