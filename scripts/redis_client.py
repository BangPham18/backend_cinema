# app/core/redis_client.py
import redis

# Redis default: localhost:6379
r = redis.Redis(
    host='redis-14536.c114.us-east-1-4.ec2.redns.redis-cloud.com',
    port=14536,
    decode_responses=True,
    username="default",
    password="WOPz560tYgi8zMZsllUvSN5DifvF8woW",
)

def set_otp(email: str, otp: str, expire_seconds: int = 300):
    r.setex(f"otp:{email}", expire_seconds, otp)

def get_otp(email: str) -> str:
    return r.get(f"otp:{email}")

def delete_otp(email: str):
    r.delete(f"otp:{email}")
