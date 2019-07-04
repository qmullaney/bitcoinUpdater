import requests
import time
from datetime import datetime

BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/bUm5jY9EbqBfvpgK4-dI_L'

def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    return float(response_json[0]['price_usd'])  # Convert the price to a floating point number

def post_ifttt_webhook(event, value):
    data = {'value1': value}  # The payload that will be sent to IFTTT service
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)  # Inserts our desired event
    requests.post(ifttt_event_url, json=data)  # Sends a HTTP POST request to the webhook URL


def main():

    highest_price = 0;
    while True:
        price = get_latest_bitcoin_price()

        # Send an emergency notification
        if price > highest_price:
            post_ifttt_webhook('bitcoin_price_emergency', price)
            highest_price = price

        time.sleep(60*60)  # Sleep for 5 minutes 

if __name__ == '__main__':
    main()
