import requests
import time

url="https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h_desc&per_page=10&page=1&sparkline=false"
response=requests.get(url)
if response.status_code!=200:
    print("Call limit exceeded!")
else:
    print("Updating...")
    print("This might take cca 5 min.")
data=response.json()



