import requests
from cachetools import cached, TTLCache
from tenacity import retry, wait_exponential, stop_after_attempt

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


@cached(cache)
def get_data(symbol):
    if symbol in cache:
        print(f"Fetching {symbol} data from cache")
    else:
        print(f"Fetching {symbol} data from API")
    return fetch_data(symbol)
