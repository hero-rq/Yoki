import hashlib

class URLShortener:
    def __init__(self):
        self.url_map = {}
        self.short_to_long = {}
        self.base_url = "http://thanks.ly/"

    def _hash_url(self, url):
        # Generate a hash for the given URL
        return hashlib.md5(url.encode()).hexdigest()[:6]

    def shorten_url(self, url: str) -> str:
        # Check if the URL has already been shortened
        if url in self.url_map:
            return self.url_map[url]
        
        # Generate a short URL
        short_hash = self._hash_url(url)
        short_url = self.base_url + short_hash
        
        # Store the mappings
        self.url_map[url] = short_url
        self.short_to_long[short_url] = url
        
        return short_url

    def retrieve_url(self, short_url: str) -> str:
        # Retrieve the original URL from the shortened version
        return self.short_to_long.get(short_url, "URL not found")

# Example usage
url_shortener = URLShortener()

long_url = "https://www.example.com/some/very/long/url"
short_url = url_shortener.shorten_url(long_url)
print("Shortened URL:", short_url)  

original_url = url_shortener.retrieve_url(short_url)
print("Original URL:", original_url)  
