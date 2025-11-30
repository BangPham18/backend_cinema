from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DB_CONNECTION_STRING = os.getenv("SUPABASE_DB_URL")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_USERNAME = os.getenv("REDIS_USERNAME")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    
    # Mail Settings
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = int(os.getenv("MAIL_PORT") or 587)
    MAIL_SERVER = os.getenv("MAIL_SERVER")
settings = Settings()
