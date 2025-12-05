import requests

url="https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h_desc&per_page=10&page=1&sparkline=false"
response=requests.get(url)
if response.status_code!=200:
    print("Call limit exceeded!")
data=response.json()

def get_prices(coin_id):
    """
    
    """
    url=f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=364"
    response=requests.get(url)
    if response.status_code==200:
        print("Gathering data...")
    else:
        raise Exception("Unable to get data now.Try again!")
    data = response.json()
    return data["prices"]
