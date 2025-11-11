# app.py
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
from config import SECRET_KEY, HOST, PORT, DEBUG
from models import init_db, SessionLocal, Order, Agent, PostRule, MessageLog
import models
from utils import scheduler

# register connectors/services
from connectors import facebook_connector, whatsapp_connector
from services.ai_assistant import generate_reply_for_text

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize DB
init_db()

# Basic routes
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/health')
def health():
    return jsonify({"status":"ok","version":"1.0.0"})

# Simple chat endpoint (for frontend or agents)
@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json() or {}
    text = data.get('message','')
    tone = data.get('tone','formal_friendly')
    reply = generate_reply_for_text(text, tone=tone)
    # record to message log
    db = SessionLocal()
    try:
        db.add(MessageLog(platform='internal', direction='outbound', content=reply))
        db.commit()
    finally:
        db.close()
    return jsonify({"reply": reply})

# Webhook endpoints (facebook/whatsapp) - simple versions
@app.route('/webhooks/facebook', methods=['GET','POST'])
def webhook_facebook():
    if request.method == 'GET':
        # verify
        verify_token = os.getenv('FB_VERIFY_TOKEN','')
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode and token == verify_token:
            return challenge
        return "Invalid verification", 403
    payload = request.get_json() or {}
    app.logger.info("FB webhook payload: %s", payload)
    # You should parse entries and changes and react according to PostRule table
    return jsonify({"status":"ok"})

@app.route('/webhooks/whatsapp', methods=['POST','GET'])
def webhook_whatsapp():
    if request.method == 'GET':
        return request.args.get('hub.challenge','')
    payload = request.get_json() or {}
    app.logger.info("WA webhook payload: %s", payload)
    # parse message and reply via AI
    return jsonify({"status":"ok"})

# Agents portal (lightweight)
@app.route('/agent/<int:agent_id>')
def agent_portal(agent_id):
    db = SessionLocal()
    agent = db.query(Agent).filter(Agent.id==agent_id).first()
    orders = db.query(Order).filter(Order.agent_id==agent_id).order_by(Order.created_at.desc()).all()
    db.close()
    return render_template('agent_portal.html', agent=agent, orders=orders)

# SocketIO events
@socketio.on('connect')
def handle_connect():
    app.logger.info("Client connected")

@socketio.on('chat_to_ai')
def handle_chat_ai(data):
    text = data.get('text','')
    reply = generate_reply_for_text(text)
    emit('chat_reply', {'reply': reply})

# Start scheduler thread
def start_scheduler():
    import time, threading
    t = threading.Thread(target=scheduler.worker_loop, args=(app, socketio), daemon=True)
    t.start()

if __name__ == '__main__':
    start_scheduler()
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG)
