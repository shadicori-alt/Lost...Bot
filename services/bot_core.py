# services/bot_core.py
# "العقل" الأساسي للمساعد: استخدام المكتبة ثم الFallback عبر OpenAI
import re
import logging
from flask import Blueprint, request, jsonify, current_app
from jinja2 import Template
from connectors.ai_connector import AIConnector
from services.ai_knowledge import best_kb_answer, add_kb_article, seed_db_from_files
from models import SessionLocal, Product, KBArticle
from typing import Tuple
import json

logger = logging.getLogger(__name__)
assistant_bp = Blueprint("assistant_bp", __name__)

# المحرك الخارجي (OpenAI wrapper)
ai = AIConnector()

# مساعد: يجيب عن الأسئلة، يدعم أوامر تعليم و تعديل اسعار
def parse_command(text: str) -> Tuple[str, dict]:
    """يميز بين أوامر خاصة (تعلم، تعديل سعر) أو 'chat' عادي.
    يرجع tuple: (intent, payload)
    """
    t = text.strip()
    # تعلم: "تعلم أن <معلومة>"
    if t.startswith("تعلم أن") or t.startswith("تعلم:") or t.startswith("تعلم "):
        content = re.sub(r'^(تعلم\s*(أن|:)?\s*)', '', t, flags=re.I).strip()
        return ("teach", {"content": content})
    # تعديل سعر: "عدّل سعر <اسم المنتج> إلى 120" أو "غير سعر <product> 120"
    m = re.search(r'(عدل|غير|غَيِّر|غير)\s+سعر\s+(.+?)\s+(?:إلى|لـ|to|=)\s+([\d\.]+)', t)
    if m:
        item = m.group(2).strip()
        price = float(m.group(3))
        return ("update_price", {"product": item, "price": price})
    # استعلام عن منتج: "كم سعر <product>"
    m2 = re.search(r'كم\s+سعر\s+(.+)', t)
    if m2:
        item = m2.group(1).strip()
        return ("ask_price", {"product": item})
    # افتراضي: chat
    return ("chat", {"text": text})

def try_local_kb_reply(text: str) -> str:
    """يحاول إرجاع رد من المكتبة المحلية"""
    ans = best_kb_answer(text)
    return ans

def update_product_price_by_name(product_name: str, new_price: float):
    """يحاول تحديث سعر المنتج في جدول Product (باسم يحتوي الاسم)"""
    db = SessionLocal()
    try:
        p = db.query(Product).filter(Product.title.ilike(f"%{product_name}%")).first()
        if not p:
            return {"status":"not_found"}
        p.price = float(new_price)
        db.commit()
        return {"status":"ok","id": p.id, "title": p.title, "price": p.price}
    except Exception as e:
        db.rollback()
        logger.exception("Price update error: %s", e)
        return {"status":"error", "error": str(e)}
    finally:
        db.close()

def find_product_price(product_name: str):
    db = SessionLocal()
    try:
        p = db.query(Product).filter(Product.title.ilike(f"%{product_name}%")).first()
        if not p:
            return None
        return {"title": p.title, "price": p.price}
    finally:
        db.close()

def call_openai_fallback(prompt: str, model: str="gpt-4"):
    # wrapper to AIConnector
    try:
        return ai.simple_chat(prompt, model=model)
    except Exception as e:
        logger.exception("OpenAI fallback error: %s", e)
        return "عذراً، خدمة الذكاء غير متاحة الآن."

# Route: health / test
@assistant_bp.route("/api/assistant/health", methods=["GET"])
def assistant_health():
    return jsonify({"status":"ok","engine":"assistant_v1"})

@assistant_bp.route("/api/assistant", methods=["POST"])
def assistant_handle():
    """
    استقبال رسالة JSON: { message: "...", role: "user"|"admin" (اختياري), tone: "formal_friendly" }
    يرد JSON: { reply: "...", action: {...} }
    """
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("message","").strip()
    role = data.get("role","user")
    tone = data.get("tone","formal_friendly")

    if not text:
        return jsonify({"reply":"اكتب سؤالاً أو أمرًا لأتمكن من المساعدة."})

    # تحقق إن DB seeded (مرة واحدة)
    try:
        seed_db_from_files()
    except Exception:
        pass

    intent, payload = parse_command(text)
    logger.info("Assistant intent=%s payload=%s", intent, payload)

    # تنفيذ أوامر خاصة
    if intent == "teach":
        content = payload.get("content","").strip()
        if not content:
            return jsonify({"reply":"يجب كتابة المعلومة بعد 'تعلم'."})
        # عنوان تلقائي قصير
        title = content[:120]
        res = add_kb_article(title=title, content=content, source="manual", tags="manual")
        if res.get("status") == "ok":
            return jsonify({"reply":"تم حفظ المعلومة في المكتبة المعرفية بنجاح ✅"})
        else:
            return jsonify({"reply":"حدث خطأ أثناء حفظ المعلومة."})

    if intent == "update_price":
        product = payload.get("product","")
        price = payload.get("price",0)
        if not product or price <= 0:
            return jsonify({"reply":"لم أفهم اسم المنتج أو السعر. تأكد من كتابة: عدّل سعر <اسم المنتج> إلى 120"})
        res = update_product_price_by_name(product, price)
        if res.get("status") == "ok":
            return jsonify({"reply": f"تم تحديث سعر '{res.get('title')}' إلى {res.get('price')} بنجاح."})
        elif res.get("status") == "not_found":
            return jsonify({"reply": "لم أعثر على منتج مطابق بهذا الاسم."})
        else:
            return jsonify({"reply": "حصل خطأ أثناء تحديث السعر."})

    if intent == "ask_price":
        product = payload.get("product","")
        info = find_product_price(product)
        if info:
            return jsonify({"reply": f"سعر {info['title']} هو {info['price']} جنيه."})
        else:
            return jsonify({"reply":"لم أجد المنتج المطلوب. تفضل أرسل اسم المنتج بالكامل أو افتح صفحة المنتجات."})

    # 1) حاول المكتبة المحلية أولًا
    kb_ans = try_local_kb_reply(text)
    if kb_ans:
        # If role is admin, show richer reply
        reply = kb_ans
        return jsonify({"reply": reply, "source":"kb"})

    # 2) إذا لم نجد إجابة، نستعمل OpenAI مع قالب مناسب
    prompt = f"""أنت مساعد دعم عملاء لمتجر لصقات طبية. أجب بصيغة { 'رسمي ودود' if role != 'admin' else 'مباشر إداري' } وباختصار واضح.
السؤال: {text}
إذا كان السؤال بيعني إجراءًا (تعديل سعر، إنشاء طلب) فاعرض الإجراء المطلوب بصيغة واضحة.
إذا لم تعرف الإجابة قل: "لم أجد إجابة سريعة، سأرسل طلب مراجعة من فريق الدعم.""""

    ai_reply = call_openai_fallback(prompt)
    # Simple post-processing: if contains JSON-like action, try to parse (not implemented fully)
    return jsonify({"reply": ai_reply, "source":"openai"})
