#!/bin/bash

. local_config.sh

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
idx_rand=$(( ( RANDOM % ${#available_urls[@]} )  + 1 ))
nama_lokasi=${available_lokasi[idx_rand]}
inputpath=${available_urls[idx_rand]}
#inputpath="http://183.91.68.83:8000/cctv-kota/cctv113.m3u8"

nowdate=$(date +'%m-%d-%Y')
nowtime=$(date +'%H:%M')
outputfile="data/screenshot_$nowdate-$nowtime.jpg"
logfile="data/log_$nowdate-$nowtime.txt"
echo "logfile path $logfile"
echo "output file $outputfile"
# ref : https://stackoverflow.com/a/27573049

echo "Attempting to get screenshot of '$nama_lokasi' on $nowdate , $nowtime" > $logfile
url_status=$(curl -sL -w "%{http_code}\\n" "$inputpath" -o /dev/null)
echo "url status $url_status"
if [ $url_status != "200" ] 
then
    echo "Url $inputpath unreacheble with HTTP status $url_status" >> $logfile
    exit 1
else
    ffmpeg -ss 00:00:01 -i $inputpath -vframes 1 -q:v 2 "$outputfile" >> $logfile
fi

# upload image to imgbb
upload_result=$(curl --location --request POST "https://api.imgbb.com/1/upload?key=$IMGBB_API_KEY" --form "image=@$outputfile")
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

# post to telegram bot
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" -d chat_id=$TELEGRAM_CHAT_ID -d text="Tangkapan CCTV di $nama_lokasi pada $nowdate pukul $nowtime WIB (lihat secara streaming di http://cctv.pekanbaru.go.id/live ) : $result_url"
