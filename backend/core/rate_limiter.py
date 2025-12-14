"""Rate limiting functionality"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from .config import settings


def get_rate_limit_key(request):
    """Get rate limit key based on IP address"""
    # In production, you might want to use user ID for authenticated users
    return get_remote_address(request)


# Initialize rate limiter
limiter = Limiter(
    key_func=get_rate_limit_key,
    default_limits=[f"{settings.RATE_LIMIT_PER_HOUR}/hour"]
)


def get_limiter():
    """Get limiter instance for dependency injection"""
    return limiter
