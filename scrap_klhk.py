#!/usr/bin/python
# -*- coding: utf-8 -*-
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import requests

url_api_klhk_pku = "http://203.73.26.177/bar/json/dataispu2.php?idstasiun=PEKANBARU"
url_api_pm25_klhk_pku = "http://202.73.26.177/bar/json2/pm25.php?id=PEKANBARU"
url_web_klhk_pku = 'http://iku.menlhk.go.id/aqms/pm25'

url_used = url_api_pm25_klhk_pku

def run():
    print 'start loading', url_used
    r = requests.get(url_used)
    if r.status_code != 200:
        return False, None, None, None
    data = r.json()
    pprint(data)

    ispu_terakhir = int(data[0]['pm25'])
    waktu_terakhir = datetime.strptime(data[0]['waktu'], '%Y-%m-%d %H:%M:%S.%f')
# pengakategorian berdasarkan tabel 8 di dokumen http://iku.menlhk.go.id/aqms/istilah
    if (ispu_terakhir > 250):
        status = 'BERBAHAYA'
    elif (ispu_terakhir > 150):
        status = 'SANGAT TIDAK SEHAT'
    elif (ispu_terakhir > 65.5):
        status = 'TIDAK SEHAT'
    elif (ispu_terakhir > 15.5):
        status = 'SEDANG'
    else:
        status = 'BAIK'

    ok = (datetime.now() - waktu_terakhir) < timedelta(hours=3)
    return (ok, ispu_terakhir, status, waktu_terakhir)

if __name__ == '__main__':

    ok, ispu_terakhir, status, waktu_terakhir = run()

    print 'ok, ispu_terakhir, status, waktu_terakhir'
    print ok, ispu_terakhir, status, waktu_terakhir

    if ok:
        post_message=u'Kondisi udara Pekanbaru saat ini : {status}, nilai ispu parameter PM 2.5 : {ispu} μg/m3 pada tanggal {tanggal} pukul {waktu}. Sumber : KLHK Pekanbaru ({url})'.format(status=status, ispu=ispu_terakhir,
                   tanggal=waktu_terakhir.strftime('%d-%m-%Y'),
                   waktu=waktu_terakhir.strftime('%H:%M'),
                   url=url_web_klhk_pku)

        print post_message.encode('utf-8')
        ## post
        import send_telegram, send_tweet
        send_telegram.send(post_message)
        send_tweet.send(post_message)
    else:
        print 'error on retrieving data'
