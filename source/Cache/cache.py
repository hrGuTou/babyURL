from source.Cache.LRU import LRU

class Cache:
    def __init__(self):
        # initialize cache with 100 url
        self.cache = LRU(100)

    def cache_put(self, longURL, shortURL):
        self.cache.put(longURL, shortURL)

    """
    :param longURL
    :returns -1: not found
             shorturl
    """
    def cache_get(self, longURL):
        return self.cache.get(longURL)

if __name__ == "__main__":
    c = Cache()
    c.cache_put("google.com", 'test')
    print(c.cache_get("google.com"))
    print(c.cache_get("baidu.com"))