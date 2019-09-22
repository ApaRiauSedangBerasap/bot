. local_config.sh

available_urls=()
a
idx_rand$(( ( RANDOM % 10 )  + 1 ))
inputpath="http://183.91.68.83:8000/cctv-kota/cctv113.m3u8"

nowtime=$(date +'%m-%d-%Y_%logH-%M')
outputfile="data/output_$nowtime.jpg"
# ref : https://stackoverflow.com/a/27573049

echo $outputfile

ffmpeg -ss 00:00:01 -i $inputpath -vframes 1 -q:v 2 "$outputfile"

# upload image to imgbb
curl --location --request POST "https://api.imgbb.com/1/upload?key=$IMGBB_API_KEY" --form "image=$outputfile" > "data/log_$nowtime.txt"
