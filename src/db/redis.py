import aioredis
from src.config import Config

JWT_EXPIRY = 3600

token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
port=Config.REDIS_PORT, db=0, decode_responses=True

)

async def add_jti_to_blocklist(jti: str):
    try:
        await token_blocklist.set(name = jti, value="revoked", ex=JWT_EXPIRY)
    except aioredis.ConnectionError as exc:
        # Surface a clearer error when Redis is down instead of blowing up later.
        raise RuntimeError("Redis is unavailable; cannot revoke token") from exc


async def token_in_blocklist(jti: str) -> bool:
    try:
        jti = await token_blocklist.get(name = jti)
    except aioredis.ConnectionError as exc:
        # Treat Redis-down as "not blocked" but loggable; change to raise if you prefer hard failure.
        return False
    return jti is not None    
