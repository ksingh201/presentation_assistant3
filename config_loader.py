# config_loader.py
from dotenv import load_dotenv
import os
import json

# Load .env variables
load_dotenv()

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Google Slides URL from config.json
with open("config.json", "r") as f:
    _cfg = json.load(f)
SLIDES_URL = _cfg.get("slides_url")

# Path to Google credentials (constant)
GOOGLE_CREDENTIALS_PATH = "google_credentials.json"

# Basic sanity check (will raise if any missing)
_missing = [k for k,v in {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "ELEVENLABS_API_KEY": ELEVENLABS_API_KEY,
    "SLIDES_URL": SLIDES_URL,
}.items() if not v]
if _missing:
    raise RuntimeError(f"Missing configuration for: {', '.join(_missing)}") 