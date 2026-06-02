# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Read both options from the .env file (with backup defaults just in case)
MODEL_FAST = os.getenv("MODEL_FAST", "gemini-3.5-flash")
MODEL_THINKING = os.getenv("MODEL_THINKING", "gemini-3.1-pro")