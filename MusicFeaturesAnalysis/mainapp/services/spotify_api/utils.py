from django.core.cache import cache

ACCESS_TTL = 60 * 15
REFRESH_TTL = 60 * 60 * 24 * 7

def cache_tokens(access_token: str, refresh_token: str, user_id: int):
    if access_token:
        cache.set(
            f"spotify:access:{user_id}",
            access_token,
            timeout=ACCESS_TTL,
        )
    
    if refresh_token:
        cache.set(
            f"spotify:refresh:{user_id}",
            refresh_token,
            timeout=REFRESH_TTL,
        )
        
def get_access_token(user_id: int):
    return cache.get(f"spotify:access:{user_id}")

def get_refresh_token(user_id: int):
    return cache.get(f"spotify:refresh:{user_id}")

def delete_tokens(user_id: int):
    cache.delete_many([
        f"spotify:access:{user_id}",
        f"spotify:refresh:{user_id}",
    ])