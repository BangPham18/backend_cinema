from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DB_CONNECTION_STRING = os.getenv("SUPABASE_DB_URL")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

settings = Settings()
