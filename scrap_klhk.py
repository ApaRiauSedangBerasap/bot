from pprint import pprint
from datetime import datetime
import requests

url_api_klhk_pku = "http://203.73.26.177/bar/json/dataispu2.php?idstasiun=PEKANBARU"
url_api_pm25_klhk_pku = "http://202.73.26.177/bar/json2/pm25.php?id=PEKANBARU"
url_web_klhk_pku = 'http://iku.menlhk.go.id/aqms/pm25'

url_used = url_api_pm25_klhk_pku
print 'start loading', url_used
r = requests.get(url_used)
data = r.json()
pprint(data)

ispu_terakhir = int(data[0]['pm25'])
waktu_terakhir = datetime.strptime(data[0]['waktu'], '%Y-%m-%d %H:%M:%S.%f')
if (ispu_terakhir > 300):
    status = 'BERBAHAYA'
elif (ispu_terakhir > 200):
    status = 'SANGAT TIDAK SEHAT'
elif (ispu_terakhir > 100):
    status = 'TIDAK SEHAT'
elif (ispu_terakhir > 50):
    status = 'SEDANG'
else:
    status = 'BAIK'

post_message='Kondisi udara Pekanbaru saat ini : {status}, nilai ispu parameter PM 2.5 : {ispu} pada tanggal {tanggal} pukul {waktu}. Sumber : KLHK Pekanbaru ({url})'.format(status=status, ispu=ispu_terakhir,
           tanggal=waktu_terakhir.strftime('%d-%m-%Y'),
           waktu=waktu_terakhir.strftime('%H:%M'),
           url=url_web_klhk_pku)

print post_message
## post to telegram
from send_telegram import send_telegram
send_telegram(post_message)

from tweet import tweet
tweet(post_message)
