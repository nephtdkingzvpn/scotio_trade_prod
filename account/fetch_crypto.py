import requests
from cachetools import TTLCache
import time

# Initialize a TTLCache with a maximum size and TTL (expire_after)
cache = TTLCache(maxsize=100, ttl=600)  # Cache size of 100 items, TTL of 60 seconds

# Function to fetch live crypto rates with caching
def get_live_crypto_rates():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin,ethereum,tether',
        'vs_currencies': 'usd'
    }

    # Generate a cache key based on URL and params
    cache_key = (url, frozenset(params.items()))

    # Check if the result is already in cache
    if cache_key in cache:
        print("Fetching from cache...")
        return cache[cache_key]

    try:
        print("Fetching from API...")
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad response status

        if response.status_code == 200:
            data = response.json()
            # Cache the response
            cache[cache_key] = {
                'bitcoin': data['bitcoin']['usd'],
                'ethereum': data['ethereum']['usd'],
                'tether': data['tether']['usd']
            }
            return cache[cache_key]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def fetch_crypto_with_caching():

    # Fetch crypto rates, retries 5 times if request fails
    for _ in range(5):
        rates = get_live_crypto_rates()
        if rates:
            # print("Crypto rates:", rates)
            return rates 
        time.sleep(5)  

    else:
        print("Failed to fetch crypto rates after multiple retries.")
        return None  # Return None if fetching fails after retries
