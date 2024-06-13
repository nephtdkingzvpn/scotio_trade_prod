import requests
import datetime
from django.http import JsonResponse
from tenacity import retry, wait_exponential, stop_after_attempt

import cachetools
cache = cachetools.TTLCache(maxsize=1, ttl=60 * 15)  # Cache data for 15 minutes

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

@retry(wait=wait_exponential(multiplier=1, min=1, max=60), stop=stop_after_attempt(5))
def fetch_aapl_data():
    url = "https://query1.finance.yahoo.com/v7/finance/chart/AAPL"
    params = {
        'range': '1mo',  # 1 month range
        'interval': '1d',  # Daily interval
        'indicators': 'quote',
        'includeTimestamps': 'true',
        'includePrePost': 'false',
        'corsDomain': 'finance.yahoo.com'
    }
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  # Raise exception for HTTP errors
    return response.json()

def get_aapl_data():
    # Check if data is in cache
    if 'aapl_data' in cache:
        print("Fetching data from cache")
        return cache['aapl_data']

    # Fetch data from the API
    data = fetch_aapl_data()
    
    # Store data in cache
    cache['aapl_data'] = data
    return data




# import requests

# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Accept': 'application/json, text/plain, */*',
#     'Accept-Language': 'en-US,en;q=0.5',
#     'Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1'
# }

# def get_aapl_data():
#     url = "https://query1.finance.yahoo.com/v7/finance/chart/AAPL"
#     params = {
#         'range': '1mo',  # 1 month range
#         'interval': '1d',  # Daily interval
#         'indicators': 'quote',
#         'includeTimestamps': 'true',
#         'includePrePost': 'false',
#         'corsDomain': 'finance.yahoo.com'
#     }
#     try:
#         response = requests.get(url, params=params, headers=HEADERS)
#         response.raise_for_status()  # Raise exception for HTTP errors
#         data = response.json()
#         return data
#     except requests.exceptions.RequestException as e:
#         print("Error fetching AAPL data:", e)
#         return None