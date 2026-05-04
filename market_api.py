import time
import requests

MARKETS_URL = (
    "https://api.coingecko.com/api/v3/coins/markets"
    "?vs_currency=usd&order=high_volume_desc&per_page=32&page=1&sparkline=false"
)

SUPPORTED_COINS = [
    "bitcoin", "ethereum", "ripple",
    "binancecoin", "solana", "tron",
    "dogecoin", "cardano", "chainlink", "avalanche-2",
]


def _get_with_retry(url: str) -> dict:
    """Fetches a URL, retrying every 60 seconds on non-200 responses."""
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        print("API rate-limited — retrying in 60 seconds...")
        time.sleep(60)


def fetch_coin_metadata() -> list[dict]:
    """
    Returns metadata (id, name, image, etc.) for the supported coins
    from the CoinGecko markets endpoint.
    """
    print("Fetching coin metadata...")
    all_coins = _get_with_retry(MARKETS_URL)
    return [coin for coin in all_coins if coin["id"] in SUPPORTED_COINS]


def fetch_coin_price_history(coin_id: str) -> list[tuple[int, float]]:
    """
    Returns a list of (timestamp_ms, price_usd) tuples for the past 364 days
    for the given coin ID.
    """
    url = (
        f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        f"/market_chart?vs_currency=usd&days=364"
    )
    print(f"Fetching price history for {coin_id}...")
    data = _get_with_retry(url)
    return data["prices"]
