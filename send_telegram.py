import os
import requests

def send(msg):
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

    telegram_url = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text='.format(
        TELEGRAM_BOT_TOKEN,
        TELEGRAM_CHAT_ID
    )
    res = requests.get(telegram_url + msg)

if __name__ == '__main__' :
    import sys
    send(sys.argv[1])

