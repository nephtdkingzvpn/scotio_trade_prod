import requests
from cachetools import cached, TTLCache
from tenacity import retry, wait_exponential, stop_after_attempt
from decimal import Decimal, ROUND_DOWN

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


# @cached(cache)
def get_live_crypto_rates():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin,ethereum,tether',
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            'bitcoin': data['bitcoin']['usd'],
            'ethereum': data['ethereum']['usd'],
            'tether': data['tether']['usd']
        }
    else:
        return None


def convert_usd_to_crypto(amount_in_usd, rates, crypto_type='bitcoin'):
    def format_amount(amount):
        if amount < 1:
            return amount.quantize(Decimal('1.000000000'), rounding=ROUND_DOWN)
        else:
            return round(amount, 2)

    conversions = {}
    
    if crypto_type == 'bitcoin' and 'bitcoin' in rates:
        btc_rate = Decimal(rates['bitcoin'])
        conversions['bitcoin'] = format_amount(Decimal(amount_in_usd) / btc_rate)
    
    elif crypto_type == 'ethereum' and 'ethereum' in rates:
        eth_rate = Decimal(rates['ethereum'])
        conversions['ethereum'] = format_amount(Decimal(amount_in_usd) / eth_rate)
    
    elif crypto_type == 'usdt' and 'tether' in rates:
        usdt_rate = Decimal(rates['tether'])
        conversions['usdt'] = format_amount(Decimal(amount_in_usd) / usdt_rate)
    
    return conversions


def convert_crypto_to_usd(amount_in_crypto, rates, crypto_type='bitcoin'):
    def format_amount(amount):
        return round(amount, 2)

    conversions = {}
    
    if crypto_type == 'bitcoin' and 'bitcoin' in rates:
        btc_rate = Decimal(rates['bitcoin'])
        conversions['bitcoin'] = format_amount(Decimal(amount_in_crypto) * btc_rate)
    
    elif crypto_type == 'ethereum' and 'ethereum' in rates:
        eth_rate = Decimal(rates['ethereum'])
        conversions['ethereum'] = format_amount(Decimal(amount_in_crypto) * eth_rate)
    
    elif crypto_type == 'usdt' and 'tether' in rates:
        usdt_rate = Decimal(rates['tether'])
        conversions['usdt'] = format_amount(Decimal(amount_in_crypto) * usdt_rate)
    
    return conversions
