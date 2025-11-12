from flask import Blueprint, request, jsonify
import logging
from services.memory_manager import save_memory, auto_learn_from_message
from services.ai_knowledge import find_best_answer, add_kb_article

assistant_bp = Blueprint("assistant", __name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@assistant_bp.route("/api/chat", methods=["POST"])
def assistant_handle():
    try:
        data = request.get_json(force=True)
        text = data.get("message", "").strip()
        role = data.get("role", "user")
        sender_id = data.get("sender_id", "guest")

        if not text:
            return jsonify({"error": "الرسالة فارغة"}), 400

        # البحث في قاعدة المعرفة
        kb_ans = find_best_answer(text)
        ai_reply = ""

        # الرد الافتراضي
        if kb_ans:
            reply = kb_ans
        else:
            reply = f"🤖 لم أجد إجابة دقيقة، لكن يمكنني البحث أو التعلم من المحادثة التالية: '{text}'"

        # حفظ المحادثة في الذاكرة
        save_memory(sender=sender_id, role=role, message=text, reply=reply)
        auto_learn_from_message(sender_id, text)

        return jsonify({
            "sender": sender_id,
            "message": text,
            "reply": reply,
            "status": "ok"
        })

    except Exception as e:
        logger.exception("Chat handling failed")
        return jsonify({"error": str(e)}), 500
