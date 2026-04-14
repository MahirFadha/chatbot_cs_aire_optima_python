import os
from dotenv import load_dotenv

load_dotenv()

WAHA_API_URL = os.getenv("WAHA_API_URL", "http://localhost:3000")
WAHA_API_KEY = os.getenv("WAHA_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")