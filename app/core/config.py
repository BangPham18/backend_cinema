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
settings = Settings()
