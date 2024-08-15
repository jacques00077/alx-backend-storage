#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import time
from functools import wraps

# Dictionary to store cache and access count
cache = {}

def cache_page(expiration_time: int):
    """
    Decorator to cache the result of the get_page function and count accesses.
    :param expiration_time: Time in seconds after which the cache expires.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            current_time = time.time()

            # Check if the URL is in cache and is not expired
            if url in cache:
                cache_entry = cache[url]
                if current_time - cache_entry['time'] < expiration_time:
                    # Increase the access count
                    cache[url]['count'] += 1
                    return cache_entry['content']
                else:
                    # If expired, remove the entry
                    del cache[url]

            # If URL is not cached or cache expired, fetch the content
            content = func(url)
            # Cache the result with current time and initialize count
            cache[url] = {
                'content': content,
                'time': current_time,
                'count': 1
            }
            return content
        return wrapper
    return decorator

@cache_page(expiration_time=10)
def get_page(url: str) -> str:
    """
    Fetches the HTML content of the specified URL.
    """
    response = requests.get(url)
    response.raise_for_status()  # Will raise an error for bad requests
    return response.text

# To check the access count of a specific URL
def get_access_count(url: str) -> int:
    if url in cache:
        return cache[url]['count']
    return 0

# To clear the cache (optional utility function)
def clear_cache():
    global cache
    cache = {}

# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.google.com"
    
    # First access (should fetch and cache)
    print("First access:")
    print(get_page(url))
    print(f"Access count: {get_access_count(url)}\n")
    
    # Second access within 10 seconds (should use cache)
    print("Second access within cache period:")
    print(get_page(url))
    print(f"Access count: {get_access_count(url)}\n")
    
    # Wait for cache to expire
    time.sleep(11)
    
    # Third access after 10 seconds (should fetch again)
    print("Third access after cache expired:")
    print(get_page(url))
    print(f"Access count: {get_access_count(url)}\n")
