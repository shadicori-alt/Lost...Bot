from flask import Flask, jsonify, request
import os
import logging

# ==========================
# 🔧 تهيئة التطبيق Flask
# ==========================
app = Flask(__name__)

# إعداد مفتاح سري من البيئة
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')

# ==========================
# 🧠 واجهات أساسية
# ==========================

@app.route('/')
def home():
    return jsonify({
        "status": "✅ Online",
        "message": "🚀 LastBot system is running successfully on Vercel!",
        "routes": {
            "/api/chat": "تجربة الذكاء الصناعي",
            "/api/health": "فحص حالة السيرفر",
            "/api/metrics": "عرض مقاييس الأداء"
        }
    })


@app.route('/api/health')
def health():
    return jsonify({"health": "ok", "uptime": "stable"})


@app.route('/api/chat', methods=['POST'])
def chat():
    """نموذج تجريبي بسيط لاستقبال رسالة من العميل"""
    data = request.get_json()
    user_msg = data.get('message', '')
    model = data.get('model', 'gpt-4')

    # هنا لاحقاً يتم دمج OpenAI أو DeepSeek
    reply = f"🤖 الرد الآلي: استقبلت رسالتك '{user_msg}' باستخدام النموذج {model}"

    return jsonify({"response": reply})


@app.route('/api/metrics')
def metrics():
    """مقاييس بسيطة لاختبار Prometheus أو المراقبة"""
    metrics_data = """
    # HELP lastbot_requests_total عدد الطلبات المستلمة
    # TYPE lastbot_requests_total counter
    lastbot_requests_total{endpoint="/api/chat"} 42

    # HELP lastbot_uptime_seconds مدة التشغيل
    # TYPE lastbot_uptime_seconds gauge
    lastbot_uptime_seconds 3600
    """
    return metrics_data, 200, {'Content-Type': 'text/plain; charset=utf-8'}


# ==========================
# 🧩 المعالجة الافتراضية للأخطاء
# ==========================
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "الصفحة غير موجودة"}), 404


@app.errorhandler(500)
def server_error(e):
    logging.exception("❌ خطأ في السيرفر:")
    return jsonify({"error": "حدث خطأ داخلي في الخادم"}), 500


# ==========================
# 🧱 لا تستخدم app.run في Vercel
# ==========================
# فقط عرّف التطبيق ليقوم Vercel بتشغيله
app = app
