import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send(msg, pictures=[]):
    if isinstance(pictures, list) and len(pictures) > 0:
        telegram_url = 'https://api.telegram.org/bot{0}/sendPhoto'.format(
            TELEGRAM_BOT_TOKEN,
        )

        for idx, pic_path in enumerate(pictures):
            res = requests.post(telegram_url, files={
                'photo': open(pic_path, 'rb'),
            }, data = {
                'chat_id' : TELEGRAM_CHAT_ID,
                'caption' : msg if idx <= 0 else None,
            })
    else:
        telegram_url = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text='.format(
            TELEGRAM_BOT_TOKEN,
            TELEGRAM_CHAT_ID
        )
        res = requests.get(telegram_url + msg)

if __name__ == '__main__' :
    import sys
    send(sys.argv[1])

