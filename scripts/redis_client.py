# app/core/redis_client.py
import redis
from app.core.config import settings

# Redis default: localhost:6379
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    username=settings.REDIS_USERNAME,
    password=settings.REDIS_PASSWORD,
)

def set_otp(email: str, otp: str, expire_seconds: int = 300):
    r.setex(f"otp:{email}", expire_seconds, otp)

def get_otp(email: str) -> str:
    return r.get(f"otp:{email}")

def delete_otp(email: str):
    r.delete(f"otp:{email}")
