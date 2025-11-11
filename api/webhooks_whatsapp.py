# api/webhooks_whatsapp.py
from flask import Blueprint, request, current_app, jsonify
from services.messenger_sender import send_whatsapp_message
from services.ai_engine import AiEngine
from models.models import SessionLocal, Order, MessageLog, Agent

bp = Blueprint('webhooks_whatsapp', __name__)
ai = AiEngine()

@bp.route('/webhook/whatsapp', methods=['GET'])
def wa_verify():
    # for verification if needed (depends on provider)
    return request.args.get('hub.challenge', '')

@bp.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_events():
    data = request.get_json()
    # parse incoming messages as provider docs
    # extract phone, message, whatsapp_message_id, etc.
    # then run NLU and respond (or route to agent)
    incoming_text = '...'  # parse accordingly
    sender_phone = '...'   # parse
    # NLU
    intent, entities = ai.parse_intent(incoming_text)
    # decide response template
    reply = ai.generate_reply(incoming_text, tone='formal_friendly')
    # send via provider
    send_whatsapp_message(sender_phone, reply)
    # log
    db = SessionLocal()
    db.add(MessageLog(platform='whatsapp', direction='inbound', content=incoming_text, meta=json.dumps({'from': sender_phone})))
    db.commit()
    db.close()
    return jsonify({'status':'ok'}), 200
