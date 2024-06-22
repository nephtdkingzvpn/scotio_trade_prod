import requests
from cachetools import TTLCache
import time

# Initialize a TTLCache with a maximum size and TTL (expire_after)
cache = TTLCache(maxsize=100, ttl=604800)  # Cache size of 100 items, TTL of 604800 seconds (1 week)

# Function to fetch crypto history with caching
def fetch_crypto_history():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': 30
    }

    # Generate a cache key based on URL and params
    cache_key = (url, frozenset(params.items()))

    # Check if the result is already in cache
    if cache_key in cache:
        print("Fetching history from cache...")
        return cache[cache_key]

    try:
        print("Fetching history from API...")
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad response status

        if response.status_code == 200:
            data = response.json()
            # Cache the response
            cache[cache_key] = data
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Function to demonstrate the usage of fetching crypto history with caching
def fetch_history_with_caching():
    # Fetch crypto history, retries 5 times if request fails
    for _ in range(5):
        crypto_history = fetch_crypto_history()
        if crypto_history:
            # print("Crypto history:", crypto_history)
            return crypto_history  # Return the fetched history
        time.sleep(5)  # Wait before retrying

    else:
        print("Failed to fetch crypto history after multiple retries.")
        return None  # Return None if fetching fails after retries


