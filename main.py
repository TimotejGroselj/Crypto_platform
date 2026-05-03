import os
import subprocess

from cli_inputs import get_int_input
from price_updater import is_price_current, update_coin_prices
from services import (
    display_todays_prices,
    get_all_coins,
    prompt_coin_graph,
    prompt_market_volume,
    run_login,
    run_register,
)

if not os.path.exists("cryptodata.sqlite"):
    subprocess.run(["python", "seed_users.py"], check=True)
    subprocess.run(["python", "create_tables.py"], check=True)
    subprocess.run(["python", "seed_data.py"], check=True)
    subprocess.run(["python", "seed_transactions.py"], check=True)

coins = get_all_coins()
for coin in coins:
    if not is_price_current(coin.get_coin_id()):
        update_coin_prices(coin.get_coin_id())

print("Welcome!")
print("Navigate menus by entering the number next to your chosen option.")

user = None
while True:
    choice = get_int_input(
        "Do you already have an account?\n1. Yes\n2. No\n3. Exit\n", 3
    )
    if choice == 1:
        user = run_login()
        if user is not None:
            break
    elif choice == 2:
        run_register()
    elif choice == 3:
        break

while user is not None:
    action = get_int_input(
        "What would you like to do?\n"
        "1. See today's prices\n"
        "2. View a price chart\n"
        "3. View your portfolio\n"
        "4. View coin market volume\n"
        "5. Deposit funds\n"
        "6. Withdraw funds\n"
        "7. Trade cryptocurrency\n"
        "8. Exit\n",
        8,
    )
    if action == 1:
        display_todays_prices(coins)
    elif action == 2:
        prompt_coin_graph(coins)
    elif action == 3:
        user.display_assets()
    elif action == 4:
        prompt_market_volume()
    elif action == 5:
        user.prompt_deposit()
    elif action == 6:
        user.prompt_withdraw()
    elif action == 7:
        user.prompt_trade()
    elif action == 8:
        break
