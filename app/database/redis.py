from redis.asyncio import Redis

from app.config import db_settings


_token_blacklist = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=0,
)
#print(f"Connected to Redis at {db_settings.REDIS_HOST}:{db_settings.REDIS_PORT}")

async def add_jti_to_blacklist(jti: str):
    await _token_blacklist.set(jti, "blacklisted")


async def is_jti_blacklisted(jti: str) -> bool:
    return await _token_blacklist.exists(jti)
