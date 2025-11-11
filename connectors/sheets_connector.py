# connectors/sheets_connector.py
# This is a placeholder. For production use google-api-python-client + oauth2.
import os
import json
from config import GOOGLE_SHEETS_CREDENTIALS_JSON, GOOGLE_SHEET_ID

def append_row(values):
    # Implement with Google Sheets API
    # Placeholder: write to local file for now
    path = "data/sheet_backup.json"
    record = {"ts": __import__('time').time(), "values": values}
    os.makedirs("data", exist_ok=True)
    arr = []
    if os.path.exists(path):
        try:
            arr = json.load(open(path))
        except Exception:
            arr = []
    arr.append(record)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(arr, f, ensure_ascii=False, indent=2)
    return {"status": "ok"}
