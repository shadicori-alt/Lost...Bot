from flask import Flask, request, jsonify
from flask_cors import CORS
from services.bot_core import assistant_bp
from models import Base, engine

# إنشاء التطبيق
app = Flask(__name__)
CORS(app)

# تسجيل Blueprint الخاص بالمساعد الذكي
app.register_blueprint(assistant_bp)

# إنشاء قاعدة البيانات في أول تشغيل
Base.metadata.create_all(bind=engine)

@app.route("/")
def home():
    return jsonify({"status": "✅ LastBot system running", "version": "1.0"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
