import os
import subprocess
from datetime import datetime

import scrap_bmkg, scrap_klhk, scrap_cctv
import send_tweet, send_telegram

curdir = os.path.dirname(os.path.realpath(__file__))
os.chdir(curdir)

ok_klhk, klhk_ispu, klhk_status, klhk_time = scrap_klhk.run()
ok_bmkg, bmkg_ispu, bmkg_status, bmkg_time = scrap_bmkg.run()
ok_cctv, cctv_location, cctv_date, cctv_time, cctv_filepath = scrap_cctv.run()

color_options = {
    'BAIK'               : 'green',
    'SEDANG'             : 'blue',
    # 'TIDAK SEHAT'        : 'yellow',
    'TIDAK SEHAT'        : '#c2c52a',
    'SANGAT TIDAK SEHAT' : 'red',
    'BERBAHAYA'          : 'black',
}

print 'results:'
print 'ok_klhk, klhk_ispu, klhk_status, klhk_time:', ok_klhk, klhk_ispu, klhk_status, klhk_time
print 'ok_bmkg, bmkg_ispu, bmkg_status, bmkg_time :',ok_bmkg, bmkg_ispu, bmkg_status, bmkg_time
print 'ok_cctv, cctv_date, cctv_time, cctv_filepath :',ok_cctv, cctv_date, cctv_time, cctv_filepath

# only post on below 2 conditions: 
# 1. at 7:00 WIB everyday and either bmkg/klhk data exists
# 2. when BMKG status is neiher BAIK/SEDANG. 
# Why BMKG only? because bmkg's PM10 data seemed to me as more stable and not 
# easily fluctuate compared to KLHK's PM2.5 data
if (datetime.now().hour == 7 and (ok_klhk or ok_bmkg)) or \
   (ok_bmkg and bmkg_status not in ['BAIK', 'SEDANG']) or \
   (not ok_bmkg and ok_klhk and klhk_status not in ['BAIK', 'SEDANG']):

    # generate chart
    text = """
var data_points = [ {klhk_ispu}, {bmkg_ispu}],
    data_colors = [ '{klhk_color}', '{bmkg_color}' ];
    data_times = [ '{klhk_time}', '{bmkg_time}' ];
"""
    text = text.format(
        klhk_ispu=klhk_ispu,
        bmkg_ispu=bmkg_ispu,
        klhk_color=color_options[klhk_status],
        bmkg_color=color_options[bmkg_status],
        klhk_time=klhk_time.strftime('%d-%m-%Y %H:%M'),
        bmkg_time=bmkg_time.strftime('%d-%m-%Y %H:%M')
    )
    
    data_path = curdir + '/chart/input_data.js'
    with open(data_path, 'wb') as f:
        f.write(text)

    os.chdir(curdir + '/chart')

    chrome_executable = os.getenv('CHROME_EXECUTABLE', 'google-chrome')
    res = subprocess.check_output([chrome_executable + ' --headless --disable-gpu --window-size=500,600 --screenshot=chart.png  index.html'], shell=True)

    # generate message
    os.chdir(curdir)

    msg = "Kondisi asap riau terakhir : "
    if ok_klhk:
        msg += "{} menurut data KLHK. ".format(klhk_status)
    if ok_bmkg:
        msg += "{} menurut data BMKG. ".format(bmkg_status)
    pics = [ curdir + '/chart/chart.png' ]

    if ok_cctv:
        pics.append(cctv_filepath)
        msg += "Foto: Tangkapan CCTV di {} pada {} pukul {}".format(cctv_location, cctv_date, cctv_time)

    print "Final message : ", msg
    print pics

    send_tweet.send(msg, pics)
    send_telegram.send(msg, pics)
