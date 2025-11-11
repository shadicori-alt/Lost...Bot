# connectors/ai_connector.py
import os
import json
from config import OPENAI_API_KEY, DEEPSEEK_API_KEY
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

class AIConnector:
    def __init__(self):
        self.openai_key = OPENAI_API_KEY
        self.client = OpenAI(api_key=self.openai_key) if OpenAI and self.openai_key else None

    def simple_chat(self, prompt, model="gpt-4", max_tokens=300, temperature=0.3):
        if not self.client:
            return "AI not configured."
        resp = self.client.chat.completions.create(
            model=model,
            messages=[{"role":"system","content":"You are an assistant."},{"role":"user","content":prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        try:
            return resp.choices[0].message.content
        except Exception:
            return str(resp)
