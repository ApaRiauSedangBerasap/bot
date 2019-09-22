. local_config.sh

available_urls=()
available_urls[0]="http://183.91.68.83:8000/cctv-kota/cctv113.m3u8" # kantor walikota pekanbaru
available_urls[1]="http://183.91.68.83:8000/cctv-kota/cctv105.m3u8" # Bank Riau Pusat
available_urls[2]="http://183.91.68.83:8000/cctv-kota/cctvPasarBawah.m3u8" # Pasar Bawah
available_urls[3]="http://183.91.68.83:8000/cctv-kota/cctvHrpRaya.m3u8" # Jl. Harapan Raya
available_urls[4]="http://183.91.68.83:8000/cctv-kota/cctv-soebrantas-garudasakti.m3u8" # Sp. Soebrantas - Garuda Sakti
available_urls[5]="http://183.91.68.83:8000/cctv-kota/cctv101.m3u8" # Terminal AKAP
idx_rand=$(( ( RANDOM % ${#available_urls[@]} )  + 1 ))
inputpath=${available_urls[idx_rand]}
#inputpath="http://183.91.68.83:8000/cctv-kota/cctv113.m3u8"

nowtime=$(date +'%m-%d-%Y_%H-%M')
outputfile="data/output_$nowtime.jpg"
logfile="data/log_$nowtime.txt"
# ref : https://stackoverflow.com/a/27573049

echo $outputfile

ffmpeg -ss 00:00:01 -i $inputpath -vframes 1 -q:v 2 "$outputfile"

# upload image to imgbb
curl --location --request POST "https://api.imgbb.com/1/upload?key=$IMGBB_API_KEY" --form "image=@$outputfile" > $logfile

echo "final url:"
cat $logfile | python -c "import sys, json; print json.load(sys.stdin)['data']['url']"
