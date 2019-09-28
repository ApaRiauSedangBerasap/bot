ApaRiauSedangBerasap Bot
============================

Program ini adalah program bot yang digunakan oleh akun-akun ApaRiauSedangBerasap. Repository ini menggunakan python dan dibuat untuk dijalankan dengan memanfaatkan scheduler cron dalam sistem operasi berbasis GNU/Linux.

Script ini secara umum melakukan beberapa hal berikut:
- men-scrapt data Konsentrasi Partikulat PM2.5 di Pekanbaru dari situs KemenLHK
- men-scrapt data Konsentrasi Partikulat PM10 di Pekanbaru dari situs BMKG
- membuat sreenshot dari cctv lalu lintas pekanbaru dari situs http://cctv.pekanbaru.go.id/live (dipilih secara random)
- membuat chart dan menarik kesimpulan soal status udara berdasarkan data dari KLHK dan BMKG
- mem-post hasilnya via channel telegram dan twitter.

Untuk menjalankan script ini, diperlukan setting environment variable yang contohnya bisa dilihat di file local_config.sh.example yang telah di sediakan. Script ini juga membutuhkan python 2.x untuk beberapa bagian nya, dan juga ada beberapa library yang perlu di install di requirements.txt.

Kode ini dipublikasikan sebagai kode Open Source dengan lisensi MIT (https://opensource.org/licenses/MIT)

Developer : Abdurrahman Shofy Adianto ( abdurrahman.adianto.id )

## Links

- Website : ApaRiauSedangBerasap.com
- Twitter : twitter.com/KondisiAsapRiau
- Channel Telegram : t.me/ApaRiauSedangBerasap

