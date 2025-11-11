# api/webhooks_fb.py
from flask import Blueprint, request, jsonify, current_app
import json
from models.models import PostRule, MessageLog, SessionLocal
from services.messenger_sender import send_private_message, post_comment_action
from services.ai_engine import AiEngine

bp = Blueprint('webhooks_fb', __name__)

@bp.route('/webhook/facebook', methods=['GET'])
def fb_verify():
    # For webhook verification
    VERIFY_TOKEN = current_app.config.get('FB_VERIFY_TOKEN')
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@bp.route('/webhook/facebook', methods=['POST'])
def fb_events():
    payload = request.get_json()
    # iterate changes
    # handle comment creation or messages
    for entry in payload.get('entry', []):
        for change in entry.get('changes', []):
            # comments on posts (page)
            if change.get('field') == 'feed':
                value = change.get('value', {})
                post_id = value.get('post_id')
                verb = value.get('verb')
                comment_id = value.get('comment_id')
                from_user = value.get('from', {})
                text = value.get('message', '')
                # find applicable rules
                db = SessionLocal()
                rules = db.query(PostRule).filter(PostRule.page_id==entry.get('id'), PostRule.active==True).all()
                for rule in rules:
                    # if post-specific rule or general page rule
                    # evaluate conditions (payload could have matchers)
                    # do action: comment or private reply or assign agent
                    # simplified example: if action_type == 'comment' -> post comment
                    pass
                db.close()

            # messages (page inbox) comes via messaging field - handle similarly (send private reply)
    return jsonify({'status':'ok'}), 200
