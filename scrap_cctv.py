#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from pprint import pprint
from datetime import datetime
import subprocess as sb
import requests

available_urls = [
    # ["http://183.91.68.83:8000/cctv-kota/cctv113.m3u8",'kantor walikota pekanbaru'],
    ["http://183.91.68.83:8000/cctv-kota/cctv105.m3u8", 'Bank Riau Pusat'],
    ["http://183.91.68.83:8000/cctv-kota/cctvPasarBawah.m3u8", 'Pasar Bawah'],
    ["http://183.91.68.83:8000/cctv-kota/cctvHrpRaya.m3u8", 'Jl. Harapan Raya'],
    ["http://183.91.68.83:8000/cctv-kota/cctv-soebrantas-garudasakti.m3u8", 'Sp. Soebrantas - Garuda Sakti'],
    ["http://183.91.68.83:8000/cctv-kota/cctv101.m3u8", 'Terminal AKAP'],
]
curtime = datetime.now()
nowdate = curtime.strftime('%d-%m-%Y')
nowtime = curtime.strftime('%H:%M')

curdir = os.path.dirname(os.path.realpath(__file__))
output_filepath = '{}/data/screenshot_{}_{}.png'.format(curdir, nowdate, nowtime)

url_used = available_urls[ datetime.now().hour % len(available_urls) ]
print 'start loading screenshot of', url_used[1]

cmd = 'ffmpeg -ss 00:00:01 -i {} -vframes 1 -q:v 2 {}'.format(url_used[0], output_filepath)
res = sb.check_output([ cmd ], shell=True)

# upload to imgbb
IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')
upload_result=requests.post("https://api.imgbb.com/1/upload?key="+IMGBB_API_KEY, files={'image' : open(output_filepath, 'r') })
result=upload_result.json()
result_url=result['data']['url']
print result_url
# result_url=result_url['data']['url']

post_message="Tangkapan CCTV di {} pada {} pukul {} WIB (lihat secara streaming di http://cctv.pekanbaru.go.id/live ) : {}".format(url_used[1], nowdate, nowtime, result_url)

print post_message.encode('utf-8')
## post to telegram
from send_telegram import send_telegram
send_telegram(post_message)

from tweet import tweet
tweet(post_message, open(output_filepath, 'rb'))
