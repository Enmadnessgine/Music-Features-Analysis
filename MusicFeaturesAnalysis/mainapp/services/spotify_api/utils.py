from django.core.cache import cache

ACCESS_TTL = 60 * 15
REFRESH_TTL = 60 * 60 * 24 * 7

def cache_tokens(access_token: str, refresh_token: str, user_id: int):
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

if __name__ == "__main__":
    test_user_id = 123
    print("=== Тест кешування токенів ===")

    # Ставимо токени
    cache_tokens("ACCESS_TEST", "REFRESH_TEST", test_user_id)
    print("Токени збережені ✅")

    # Отримуємо токени
    access = get_access_token(test_user_id)
    refresh = get_refresh_token(test_user_id)
    print(f"Access token: {access}")
    print(f"Refresh token: {refresh}")

    # Видаляємо токени
    delete_tokens(test_user_id)
    print("Токени видалені ✅")

    # Перевіряємо після видалення
    access_after = get_access_token(test_user_id)
    refresh_after = get_refresh_token(test_user_id)
    print(f"Access token після видалення: {access_after}")
    print(f"Refresh token після видалення: {refresh_after}")