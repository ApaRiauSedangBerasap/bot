#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime
import json

import bs4
from bs4 import BeautifulSoup
import requests

curdir = os.path.dirname(os.path.realpath(__file__))
os.chdir(curdir)

# retrieve latest data
url_bmkg_pku = 'https://bmkg.go.id/kualitas-udara/informasi-partikulat-pm10.bmkg?Lokasi=PEKANBARU'

url_used = url_bmkg_pku

def run():
    oke, ispu_terakhir, status, jam_terakhir = False, None, None, None
    print 'start loading', url_used
    r = requests.get(url_used, verify=False) # important, turned off ssl verification. see : https://2.python-requests.org/en/master/user/advanced/#ssl-cert-verification
    if r.status_code != 200 :
        print 'status code', r.status_code
        return False, None, None, None

    page_content = r.text

    # parse retrieved page
    soup = BeautifulSoup(page_content, 'html.parser')
    script_elements = soup.select('script')
    js_content = [ i for i in script_elements \
            if len(i.contents) > 0 and ".highcharts" in i.contents[0] ]
    js_content = js_content[0]

# parse template file
    bmkg_filepath='bmkg/bmkg.html'
    with open(bmkg_filepath, 'r') as f:
        t = f.readlines()
    soup = BeautifulSoup("".join(t), 'html.parser')
    elm = soup.select_one('#scriptPEKANBARU')
    elm.string = js_content.string
# print 'elm', elm
# print elm.contents
    for i in elm.children:
        if isinstance(i, bs4.element.Tag):
            i.extract()
# elm.a.extract()
# print type(elm.a)

# print soup.prettify().encode('utf-8')
    temp_bmkg_filepath='bmkg/temp_bmkg_replaced.html'
    with open(temp_bmkg_filepath, 'w') as f:
        f.write(soup.prettify().encode('utf-8'))

# re-parse replaced page using google-chrome headless
    os.chdir('bmkg')

# ref on google chrome headless usage: https://developers.google.com/web/updates/2017/04/headless-chrome
    chrome_executable = os.getenv('CHROME_EXECUTABLE', 'google-chrome')
    res = subprocess.check_output([chrome_executable + ' --headless --disable-gpu --window-size=1280,768 --dump-dom  temp_bmkg_replaced.html'], shell=True)
# print res

# final parsing using beautiful soup
    soup = BeautifulSoup(res, 'html.parser')
    final_data = soup.select_one('#parsed_data')
    final_data = json.loads(final_data.text)
    print 'final data :', final_data

    ispu_terakhir = final_data[-1]
    jam_terakhir = len(final_data)

    # pengakategorian berdasarkan situs bmkg yang jadi acuan url
    if (ispu_terakhir > 350):
        status = 'BERBAHAYA'
    elif (ispu_terakhir > 250):
        status = 'SANGAT TIDAK SEHAT'
    elif (ispu_terakhir > 150):
        status = 'TIDAK SEHAT'
    elif (ispu_terakhir > 50):
        status = 'SEDANG'
    else:
        status = 'BAIK'
    
    return (True, ispu_terakhir, status, jam_terakhir)

if __name__ == '__main__':
    ok, ispu_terakhir, status, jam_terakhir = run()

    print 'ok, ispu_terakhir, status, jam_terakhir'
    print ok, ispu_terakhir, status, jam_terakhir

    if ok:
        post_message=u'Kondisi udara Pekanbaru saat ini : {status}, konsentrasi partikulat PM10 dari BMKG Pekanbaru : {ispu} μg/m3 pada hari ini pukul {jam}:00 WIB. Sumber : BMKG Pekanbaru ({url})'.format(status=status, 
            ispu=ispu_terakhir,
            jam=jam_terakhir,
            url=url_used)

        print post_message.encode('utf-8')
        ## post
        import send_telegram, send_tweet
        send_telegram.send(post_message)
        send_tweet.send(post_message)
    else:
        print 'error on retrieving data'
