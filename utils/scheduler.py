# utils/scheduler.py
import threading
import time
from config import POLL_SECONDS
from services.ai_assistant import generate_reply_for_text
from connectors.facebook_connector import post_comment
from models import SessionLocal, PostRule, Order

_running = False

def worker_loop(app, socketio):
    global _running
    if _running:
        return
    _running = True
    while True:
        try:
            # Placeholder: poll DB/rules or external queues
            # Example: check for pending auto-comments creation tasks in DB
            # Here we just sleep to reduce CPU usage
            time.sleep(POLL_SECONDS)
        except Exception as e:
            app.logger.exception("Scheduler loop error: %s", e)
            time.sleep(POLL_SECONDS)
