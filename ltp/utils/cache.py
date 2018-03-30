"""
HTTP Caching methods
"""

class CacheMissErrorError(Exception):
    def __init__(self, url):
        self.msg = "URL not found: {}".format(url)
        self.url = url

class CacheItem(object):
    """
    Representation of a cached item
    """

    def __init__(self, url, headers, data):
        """
        Create a new cache item
        url: str or list of urls that this item maps to
        """

        self.data = data
        self.headers = headers

        if isinstance(url, str):
            self.urls = [url]
        else:
            self.urls = url

    def __repr__(self):
        url_string = self.urls[0]
        if len(url_string) > 32:
            url_string = url_string[:29] + '...'

        return "CacheItem: {} bytes data. URL: {}".format(len(self.data),
                                                          url_string)


class DictCache(object):
    """
    Simple cache using python dictionary
    """

    def __init__(self):
        """
        Initialize the cache
        """
        self.items = []

    def __repr__(self):
        return "DictCache of {} items".format(len(self.items))

    def __iter__(self):
        self.__idx = 0
        return self

    def __next__(self):
        if self.__idx >= len(self.items):
            raise StopIteration
        self.__idx += 1
        return self[self.__idx - 1]

    def __getitem__(self, url: str):
        """
        Fetches an item from the cache by URL.
        """

        if isinstance(url, str):
            try:
                return [i for i in self.items if i.urls == url][0]
            except IndexError:
                raise CacheMissErrorError("URL not found in cache: {}"
                                          "".format(url))
        else:
            idx = url
            return self.items[idx]


    def __iadd__(self, item: CacheItem):
        if not isinstance(item, CacheItem):
            raise TypeError("Expected a CacheItem, received: {}".format(
                type(item)))
        if item not in self.items:
            self.items.append(item)
        return self

    def __delitem__(self, item: CacheItem):
        """__delitem___(str) -> DictCache: Remove a CacheItem from the cache"""
        if not isinstance(item, CacheItem):
            raise TypeError("Expected a CacheItem, received: {}".format(
                type(item)))
        if item not in self.items:
            raise CacheMissErrorError("Cache Item not found : {}".format(item))
        return self

    def get(self, url: str):
        """get(str) -> DictCache: Get an item from the cache by url."""
        if not isinstance(url, str):
            raise TypeError("Expected a url string, received: {}".format(
                type(url)))
        return self.__getitem__(url)

    def add(self, item: CacheItem):
        """add(CacheItem) -> DictCache: Add an item to the cache."""
        return self.__iadd__(item)

    def remove(self, item: [str, CacheItem]):
        """remove(str or CacheItem) -> DictCache: Remove a cached item."""
        if isinstance(item, str):
            try:
                i = [i for i in self.items if i.urls == item][0]
                return self.__delitem__(i[0])
            except IndexError:
                raise CacheMissErrorError("URL not in cache: {}".format(item))
        elif isinstance(item, CacheItem):
            self.__delitem__(item)

def gen_ci():
    import random, string
    s = ''.join([random.choice(string.ascii_letters) for i in range(8)])
    url = "http://{}.com/".format(s)
    headers = {'Host': s + '.com'}
    data = ''.join([random.choice(string.printable) for i in range(1024)])
    return CacheItem(url, headers, data)

c = DictCache()
ci = CacheItem('http://www.google.com/', {}, "<html></html>")

