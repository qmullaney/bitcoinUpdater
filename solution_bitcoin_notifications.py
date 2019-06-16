import requests
import time
from datetime import datetime

BITCOIN_PRICE_THRESHOLD = 10000
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

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')  # Formats the date into a string: '24.02.2018 15:09'
        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        row = '{}: $<b>{}</b>'.format(date, price)  # 24.02.2018 15:09: $<b>10123.4</b>
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    return '<br>'.join(rows)  # Join the rows delimited by <br> tag: row1<br>row2<br>row3

def main():
    bitcoin_history = []
    highest_price = 0;
    while True:
        price = get_latest_bitcoin_price()

        # Send an emergency notification
        if price > highest_price:
            post_ifttt_webhook('bitcoin_price_emergency', price)
            highest_price = price
    
        time.sleep(30)  # Sleep for 5 minutes (for testing purposes you can set it to a lower number)

if __name__ == '__main__':
    main()
