import sys

import json
import time

from plyer import notification
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

##############################
# SETUP:
##############################
allPurchasedPrices = dict()
allPurchasedPrices['BTC'] = 8833.89477
allPurchasedPrices['LTC'] = 40
allPurchasedPrices['DASH'] = 71.482012
# allPurchasedPrices['ETH'] = 181.184616

previousCheck = dict()
previousCheck['BTC'] = 8833.89477
previousCheck['LTC'] = 40
previousCheck['DASH'] = 71.482012
# previousCheck['ETH'] = 181.184616

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

parameters = {
  'convert':'USD',
  'symbol': 'BTC,LTC,DASH'
}

# Secret key
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '',
}

WHEN_TO_SELL_ = 2

DELAY = 300
##############################
# SETUP
##############################


x = input("Check once or repeatedly? (Enter 1 for once or anything else for repeatedly): ")
if x == "1":
    once = True
else:
    once = False

if __name__ == "__main__":
    session = Session()
    session.headers.update(headers)
    ctr = 1
    while True:
        print(f"Checked {ctr} times:")
        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            print(f"Success! Cost: {data['status']['credit_count']} credit(s).")
            data = data['data']
            
            for item in data.values():
                name = item['name']
                symbol = item['symbol']
                price = item['quote']['USD']['price']
                purchasedPrice = allPurchasedPrices[symbol]
                percent = round((100 * (price / purchasedPrice )), 2)
                print("\t{: <8}:\t{: <15} ({: <4}%)".format(name, price, percent))

                if purchasedPrice <= price:
                    if price >= ( purchasedPrice * WHEN_TO_SELL_):
                        print(f"\n\t\tSell {name} ({symbol}). Price: {price} ({round((percent-100), 2)}% profit)\n")

                        notification.notify(
                            title=f"Sell {name}",
                            message=f"Sell {name}",
                            app_icon=None,
                            timeout=10,
                        )

                        allPurchasedPrices[symbol] = price
                        cont = input("Press 'Q' to stop or press enter to continue: ")
                        if cont.lower() == "q":
                            sys.exit()
                        else:
                            print("Continuing. . .")
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        if once:
            break
        else:
            time.sleep(DELAY)
            ctr += 1
            print("="*75)
