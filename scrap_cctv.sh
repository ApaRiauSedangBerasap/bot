#!/bin/bash

mydir=$(dirname "$0") # ref : https://unix.stackexchange.com/a/273347

. $mydir/local_config.sh

# ====== DEFINITION OF STREAMING URL =========
# repsitory ini memanfaatkan link .m3u8 yang cukup populer untuk situs-situs cctv
# publik. saya mendapatkan link-link dibawah ini dengan melihat source code halaman
# dari http://cctv.pekanbaru.go.id/live
available_urls=()
available_urls[0]="http://183.91.68.83:8000/cctv-kota/cctv113.m3u8" # kantor walikota pekanbaru
available_urls[1]="http://183.91.68.83:8000/cctv-kota/cctv105.m3u8" # Bank Riau Pusat
available_urls[2]="http://183.91.68.83:8000/cctv-kota/cctvPasarBawah.m3u8" # Pasar Bawah
available_urls[3]="http://183.91.68.83:8000/cctv-kota/cctvHrpRaya.m3u8" # Jl. Harapan Raya
available_urls[4]="http://183.91.68.83:8000/cctv-kota/cctv-soebrantas-garudasakti.m3u8" # Sp. Soebrantas - Garuda Sakti
available_urls[5]="http://183.91.68.83:8000/cctv-kota/cctv101.m3u8" # Terminal AKAP
available_lokasi=(
 "Kantor Walikota Pekanbaru"
 "Kantor Bank Riau Pusat"
 "Pasar Bawah"
 "Jl. Harapan Raya"
 "Sp. Soebrantas - Garuda Sakti"
 "Terminal AKAP"
)

elnum=${#available_urls[@]}
idx_rand=$(python -c "import random; print random.randrange(0,$elnum)")
nama_lokasi=${available_lokasi[idx_rand]}
inputpath=${available_urls[idx_rand]}
nowdate=$(date +'%d-%m-%Y')
nowtime=$(date +'%H:%M')
screenshot_file="$mydir/data/screenshot_$nowdate-$nowtime.jpg"
logfile="$mydir/data/log_$nowdate-$nowtime.txt"
# ref : https://stackoverflow.com/a/27573049

echo "input path $inputpath"
echo "nama lokasi $nama_lokasi"
echo "logfile path $logfile"
echo "output file $screenshot_file"

echo "Attempting to get screenshot of '$nama_lokasi' on $nowdate , $nowtime" > $logfile
url_status=$(curl -sL -w "%{http_code}\\n" "$inputpath" -o /dev/null)
echo "url status $url_status"
if [ $url_status != "200" ] 
then
    echo "Url $inputpath unreacheble with HTTP status $url_status" >> $logfile
    exit 1
else
    ffmpeg -ss 00:00:01 -i $inputpath -vframes 1 -q:v 2 "$screenshot_file" >> $logfile
fi

# upload image to imgbb
upload_result=$(curl --location --request POST "https://api.imgbb.com/1/upload?key=$IMGBB_API_KEY" --form "image=@$screenshot_file")
result_url=$(echo $upload_result | python -c "import sys, json; print json.load(sys.stdin)['data']['url']" || echo "FAILED")
echo "final url: $result_url"

if [ $result_url = "FAILED" ]
then
    echo "Erron on uploading image to imagebb" >> $logfile
    echo $upload_result >> $logfile
    exit 1
else
    echo $upload_result >> $logfile
fi

post_message="Tangkapan CCTV di $nama_lokasi pada $nowdate pukul $nowtime WIB (lihat secara streaming di http://cctv.pekanbaru.go.id/live ) : $result_url"

# post to telegram bot
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" -d chat_id=$TELEGRAM_CHAT_ID -d text="$post_message"

# post to twitter
python tweet.py "$post_message" "$screenshot_file"

# ========= DOWNLOAD DATA BMKG =======================================
url_bmkg="http://www.bmkg.go.id/kualitas-udara/informasi-partikulat-pm10.bmkg?Lokasi=PEKANBARU" 
wget $url_bmkg -O "$mydir/data/data_bmkg_$nowdate-$nowtime.html"

