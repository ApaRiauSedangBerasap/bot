ApaRiauSedangBerasap Scrapper
============================

Program ini adalah program scrapper yang digunakan oleh akun-akun ApaRiauSedangBerasap. Repository ini menggunakan script bash dan dibuat untuk dijalankan dengan memanfaatkan scheduler cron dalam sistem operasi berbasis GNU/Linux.

Script ini secara umum melakukan beberapa hal berikut:
- membuat sreenshot dari cctv lalu lintas pekanbaru dari situs http://cctv.pekanbaru.go.id/live (dipilih secara random)
- mengupload file screenshot tersebut ke layanan image hosting imgbb.com
- mengirimkan notifikasi via telegram bot dengan akun yang kita simpan
- mendownload cuplikan situs https://www.bmkg.go.id/kualitas-udara/informasi-partikulat-pm10.bmkg?Lokasi=PEKANBARU

Untuk menjalankan script ini, diperlukan file local_config.sh , silahkan rename dari file local_config.sh.example yang telah di sediakan. Script ini juga membutuhkan python 2.x untuk beberapa bagian nya.

Kode ini dipublikasikan sebagai kode Open Source dengan lisensi MIT (https://opensource.org/licenses/MIT)

Developer : Abdurrahman Shofy Adianto ( abdurrahman.adianto.id )
