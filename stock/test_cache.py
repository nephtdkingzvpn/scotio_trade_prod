from cachetools import TTLCache, cached
from tenacity import retry, wait_exponential, stop_after_attempt
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Cache configuration: cache up to 100 items, each for 1 hour
cache = TTLCache(maxsize=100, ttl=3600)

@retry(wait=wait_exponential(multiplier=1, min=1, max=60), stop=stop_after_attempt(5))
def fetch_data(symbol):
    url = f"https://query1.finance.yahoo.com/v7/finance/chart/{symbol}"
    params = {
        'range': '1mo',  # 1 month range
        'interval': '1d',  # Daily interval
        'indicators': 'quote',
        'includeTimestamps': 'true',
        'includePrePost': 'false',
        'corsDomain': 'finance.yahoo.com'
    }
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def normalize_symbol(symbol):
    return symbol.lower()

@cached(cache, key=normalize_symbol)
def get_data(symbol):
    try:
        normalized_symbol = normalize_symbol(symbol)

        if normalized_symbol in cache:
            print(f"Fetching {symbol} data from cache")
            return cache[normalized_symbol]
        else:
            print(f"Fetching {symbol} data from API")
            data = fetch_data(symbol)
            cache[normalized_symbol] = data  # Store data in cache with normalized symbol
            return data
    except Exception as e:
        print(f"Error getting {symbol} data: {e}")
        return None

# Example usage
if __name__ == "__main__":
    try:
        symbol = 'AAPL'

        # Fetch data and print result
        data = get_data(symbol)
        if data:
            print(f"Data for {symbol}: {data}")
        else:
            print(f"Failed to fetch data for {symbol}")

        # Print cache content for verification
        print(f"Cache content: {list(cache.keys())}")
        print(f"Cache items: {list(cache.items())}")

    except Exception as e:
        print(f"Error in main execution: {e}")
