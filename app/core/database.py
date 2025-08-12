from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings  # Đọc từ file config (dùng dotenv)
import psycopg
from psycopg.rows import dict_row
from app.core.config import settings  # chứa DB_CONNECTION_STRING

# Kết nối Supabase
engine = create_engine(settings.DB_CONNECTION_STRING)

# Base class ORM
Base = declarative_base()

# Session local
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()

def get_connection():
    return psycopg.connect(settings.DB_CONNECTION_STRING, row_factory=dict_row)


