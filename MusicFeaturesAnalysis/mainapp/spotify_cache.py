from spotipy.cache_handler import CacheHandler

class NullCacheHandler(CacheHandler):
    def get_cached_token(self):
        return None

    def save_token_to_cache(self, token_info):
        pass
