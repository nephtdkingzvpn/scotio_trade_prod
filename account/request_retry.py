import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from time import sleep


def requests_retry_session(retries=5, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        max_backoff=30
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session



import requests
from cachetools import TTLCache
import time

# Initialize a TTLCache with a maximum size and TTL (expire_after)
cache = TTLCache(maxsize=100, ttl=60)  # Cache size of 100 items, TTL of 60 seconds

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
        return cache[cache_key]

    try:
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

# Example usage with caching and simplified retry logic
def example_usage_with_caching():
    # Fetch crypto rates, retries 5 times if request fails
    for _ in range(5):
        crypto_rates = get_live_crypto_rates()
        if crypto_rates:
            print("Crypto rates:", crypto_rates)
            break
        time.sleep(5)  # Wait before retrying

    else:
        print("Failed to fetch crypto rates after multiple retries.")

example_usage_with_caching()

