import requests
import time

url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=high_volume_desc&per_page=32&page=1&sparkline=false"
response=requests.get(url)
#naredu da mava ta znane pa vazne coine (usaj zame lolz)
populars = ['bitcoin', 'ethereum', 'ripple',
            'binancecoin', 'solana', 'tron',
            'dogecoin', 'cardano','chainlink','avalanche-2']

while True:
    response=requests.get(url)
    if response.status_code==200:
        print("Gathering data...")
        break
    else:
        print("api dick")
        time.sleep(60)

data = []
curr_price = []
for coin in response.json():
    if coin['id'] in populars:
        data.append(coin)


def get_prices(coin_id):
    """
    
    """
    url=f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=364"
    while True:
        response=requests.get(url)
        if response.status_code==200:
            print("Gathering data...")
            break
        else:
            print("api dick")
            time.sleep(60)
            
    data = response.json()
    return data["prices"]


