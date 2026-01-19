# Proposal Proyek UAS Praktikum Pemrograman Visual
## Implementasi Aplikasi Network Scanner dan Ping Monitor untuk Meningkatkan Keamanan Jaringan Lokal

**Nama:** [Nama Anda]  
**NIM:** [NIM Anda]  
**Kelas:** [Kelas Anda]  
**Mata Kuliah:** Praktikum Pemrograman Visual  

**Dosen Pengampu:** [Nama Dosen]  
**Tahun Akademik:** 2025/2026  
**Tanggal:** 13 Januari 2026  

---

## Ringkasan
Proyek ini mengusulkan pengembangan aplikasi desktop **Network Scanner & Ping Monitor** berbasis Python yang bertujuan membantu pengguna melakukan pemindaian host pada jaringan lokal serta memantau ketersediaan (availability) perangkat secara berkala. Aplikasi dibangun menggunakan **PySide6 (Qt for Python)** untuk antarmuka grafis, memanfaatkan **multithreading** melalui `QThreadPool` agar proses pemindaian tetap responsif, dan menyimpan histori hasil pemindaian ke **SQLite** agar dapat ditinjau kembali melalui fitur **Log Viewer**.

Output utama yang diharapkan adalah aplikasi GUI yang mampu:
1. Mendeteksi perangkat **online** pada suatu rentang IP (host discovery berbasis ping).
2. Melakukan **ping monitoring** beberapa IP dengan interval yang dapat diatur.
3. Mencatat hasil (status/latensi dan informasi dasar perangkat) ke database serta menyediakan fitur filter dan ekspor.

---

## 1. Pendahuluan

### 1.1 Latar Belakang
Keamanan dan ketersediaan jaringan lokal (LAN) sangat dipengaruhi oleh kemampuan pengelola jaringan untuk mengetahui perangkat yang aktif dan memantau stabilitas koneksi. Dalam praktiknya, pengecekan perangkat online/offline sering dilakukan secara manual atau menggunakan alat yang tidak ramah bagi pengguna pemula. Selain itu, tanpa pencatatan histori, sulit untuk melakukan evaluasi kestabilan koneksi dari waktu ke waktu.

Dengan memanfaatkan pemindaian berbasis **ICMP ping** (atau perintah `ping` sistem) dan monitoring berkala, aplikasi ini diharapkan menjadi alat bantu sederhana namun efektif untuk meningkatkan visibilitas jaringan lokal: perangkat apa saja yang aktif, bagaimana latensinya, dan bagaimana kondisi perangkat berubah dalam periode tertentu.

### 1.2 Rumusan Masalah
1. Bagaimana merancang aplikasi GUI yang mampu menerima input rentang IP dan melakukan pemindaian host secara cepat tanpa membuat UI “freeze”?
2. Bagaimana melakukan ping monitoring untuk beberapa IP dengan interval tertentu serta menampilkan hasilnya secara real-time?
3. Bagaimana menyimpan histori hasil scan/monitoring ke database SQLite dan menampilkan kembali data tersebut melalui log viewer yang dapat difilter?

### 1.3 Tujuan
1. Mengimplementasikan aplikasi **Network Scanner** untuk mendeteksi host online pada jaringan lokal berdasarkan rentang IP.
2. Mengimplementasikan **Ping Monitor** untuk memantau beberapa alamat IP secara berkala.
3. Mengimplementasikan penyimpanan histori hasil pemindaian ke **SQLite** dan menampilkan log yang dapat difilter serta diekspor.
4. Menerapkan pemisahan modul (mirip pola MVC) agar kode lebih terstruktur dan mudah dirawat.

### 1.4 Manfaat
- **Bagi pengguna:** memperoleh informasi perangkat online serta kestabilan koneksi tanpa proses manual yang memakan waktu.
- **Bagi pembelajaran:** melatih penerapan GUI (PySide6), multithreading di aplikasi desktop, modularisasi kode (MVC), serta integrasi database.

---

## 2. Ruang Lingkup dan Batasan

### 2.1 Ruang Lingkup
Aplikasi mencakup tiga area fungsi utama:
1. **Scanner:** pemindaian host pada rentang IP dan menampilkan perangkat yang terdeteksi online beserta informasi dasar.
2. **Ping Monitor:** pemantauan beberapa IP secara berkala dengan interval yang dapat diatur.
3. **Log Viewer:** peninjauan histori hasil scan/monitoring yang tersimpan di SQLite, disertai filter dan ekspor data.

### 2.2 Batasan
1. Pemindaian berfokus pada **host discovery** (online/offline/timeout) dan bukan pemindaian port atau eksploitasi layanan.
2. Informasi perangkat (hostname, MAC, perkiraan OS) bersifat **best-effort** dan dapat dipengaruhi firewall, konfigurasi DNS, serta aturan jaringan.
3. Target penggunaan difokuskan pada jaringan lokal dan penggunaan yang memiliki izin (authorized).

---

## 3. Analisis Kebutuhan

### 3.1 Kebutuhan Fungsional
1. Sistem menerima input rentang IP dengan format umum (contoh: `192.168.1.1-254` atau `192.168.1.10-20`).
2. Sistem melakukan ping ke setiap IP dalam rentang untuk menentukan status host:
   - **Online** jika ping berhasil.
   - **Offline** jika ping gagal.
   - **Timeout** jika melebihi batas waktu.
3. Sistem menampilkan hasil scan pada tabel (minimal): IP, Hostname, MAC Address, OS Type, Status, Latency.
4. Sistem menyediakan fitur **Start/Stop Scan** dan progress bar pemindaian.
5. Sistem memungkinkan pengguna menambahkan IP dari hasil scan ke daftar **Ping Monitor**.
6. Sistem menjalankan monitoring berkala dengan interval 1–300 detik dan memperbarui tabel monitoring.
7. Sistem menyimpan hasil scan/monitoring ke database SQLite.
8. Sistem menyediakan tampilan **Log Viewer** dengan kemampuan filter (IP, status, tanggal) dan aksi ekspor data.

### 3.2 Kebutuhan Non-Fungsional
1. **Responsif:** proses scan/monitoring tidak membekukan UI (menggunakan thread pool).
2. **Kinerja:** pemindaian dilakukan paralel dengan jumlah thread maksimal untuk mencegah overload.
3. **Keandalan data:** operasi database aman untuk akses bersamaan (thread-safe) menggunakan lock.
4. **Usability:** tampilan tab terpisah untuk Scanner, Ping Monitor, dan Log Viewer.
5. **Portabilitas:** target utama Windows, namun struktur perintah ping mempertimbangkan platform lain.

---

## 4. Teknologi yang Digunakan
- **Bahasa Pemrograman:** Python 3.x
- **GUI Framework:** PySide6 (Qt)
- **Database:** SQLite3
- **Ekspor Excel:** openpyxl (opsional, digunakan untuk ekspor `.xlsx`)
- **Library/Modul Sistem:**
  - `subprocess` untuk menjalankan `ping` dan `arp`
  - `socket` untuk reverse DNS (hostname)
  - `re` untuk parsing output
  - `QThreadPool`/`QRunnable` untuk multithreading

---

## 5. Desain dan Arsitektur Sistem

### 5.1 Arsitektur Modular (Mirip MVC)
Aplikasi diorganisasi menjadi modul:
- **UI / View:** menangani tampilan, event klik, tabel, progress bar.
- **Controller:** menangani proses pemindaian (worker per-IP) dan mengirim hasil ke UI melalui signal.
- **Model:** menangani penyimpanan dan pengambilan data log dari SQLite.
- **Config:** menyimpan konstanta agar pengaturan terpusat.

### 5.2 Alur Proses Scan Host
1. Pengguna memasukkan rentang IP pada tab Scanner.
2. Sistem memvalidasi format input rentang IP.
3. Sistem membuat tugas pemindaian untuk setiap IP (`ScanWorker`) dan mengeksekusinya di `QThreadPool`.
4. Setiap worker menjalankan `ping` dengan timeout singkat, kemudian:
   - mengambil **latensi** dari output,
   - mencoba **hostname** via reverse DNS,
   - mencoba **MAC address** via ARP cache,
   - memperkirakan **OS type** via nilai TTL (jika tersedia).
5. UI menerima hasil melalui signal, memperbarui tabel/progress, dan menyimpan log ke SQLite.

### 5.3 Alur Proses Ping Monitor
1. Pengguna menambahkan satu/lebih IP ke daftar monitoring.
2. Pengguna menentukan interval (detik) dan menekan Start Monitoring.
3. Timer menjalankan pemindaian berkala; setiap interval memicu worker ping ke tiap IP.
4. UI memperbarui status/latensi/last check pada tabel monitoring serta menyimpan log.

---

## 6. Rencana Implementasi

### 6.1 Tahapan Pekerjaan
1. **Analisis kebutuhan & desain UI:** menentukan komponen tab, tabel, dan alur penggunaan.
2. **Implementasi scanning host:** worker ping per IP, parsing hasil, dan update UI.
3. **Implementasi ping monitoring:** timer + worker, update tabel monitoring.
4. **Implementasi database logging:** schema SQLite, insert/fetch, filter log.
5. **Fitur pendukung:** ekspor CSV/Excel, clear history, mode gelap.
6. **Packaging & dokumentasi:** build aplikasi (misalnya dengan PyInstaller) dan penulisan laporan/panduan.

### 6.2 Strategi Responsivitas
- Menggunakan `QThreadPool` untuk menjalankan banyak tugas ping secara paralel.
- Membatasi jumlah thread maksimum agar tidak overload.
- Mengurangi refresh log viewer agar tidak terlalu sering saat monitoring berjalan.

---

## 7. Rencana Pengujian

### 7.1 Skenario Uji Fungsional
1. Validasi input IP range (format benar/salah, range pendek/panjang).
2. Scan pada jaringan lokal yang berisi beberapa perangkat aktif.
3. Verifikasi hasil status (Online/Offline/Timeout) dan progress bar.
4. Menambahkan IP ke Ping Monitor dan memulai monitoring.
5. Mengubah interval monitoring dan memastikan timer bekerja.
6. Membuka Log Viewer, melakukan filter berdasarkan IP/status/tanggal.
7. Ekspor log ke CSV dan Excel (jika openpyxl terpasang).
8. Hapus histori log dan memastikan data pada database kosong.

### 7.2 Kriteria Keberhasilan
- Aplikasi tidak freeze saat scan atau monitoring.
- Hasil scan/monitoring tercatat pada SQLite dan dapat ditampilkan kembali.
- Ekspor menghasilkan file yang terbaca dan sesuai dengan tabel log.

---

## 8. Jadwal Pelaksanaan (Contoh 4 Minggu)
1. **Minggu 1:** Analisis kebutuhan, desain UI, perancangan database.
2. **Minggu 2:** Implementasi scan host + progress + tampilan hasil.
3. **Minggu 3:** Implementasi ping monitor + logging + log viewer + filter.
4. **Minggu 4:** Ekspor, uji coba, perbaikan bug, packaging, finalisasi dokumentasi.

---

## 9. Risiko dan Mitigasi
1. **Hasil ping tidak akurat karena firewall/ICMP diblok:** jelaskan sebagai batasan, gunakan timeout dan status “Timeout/Offline”.
2. **Overload resource saat scan range besar:** batasi thread pool dan tampilkan peringatan untuk scan sangat besar.
3. **UI lambat saat monitoring lama:** throttle refresh log viewer dan optimalkan update tabel.
4. **Data race saat banyak thread menulis DB:** gunakan lock untuk operasi insert/clear.

---

## 10. Luaran (Deliverables)
1. Source code aplikasi (struktur modular: UI/Controller/Model/Config).
2. File database SQLite yang berisi histori hasil pemindaian.
3. File executable hasil build (jika diminta pada UAS).
4. Dokumentasi penggunaan (ringkas) dan screenshot UI untuk pelaporan.

---

## 11. Penutup
Dengan adanya aplikasi Network Scanner dan Ping Monitor berbasis GUI ini, diharapkan pengguna dapat lebih mudah melakukan pemantauan jaringan lokal serta memiliki histori untuk evaluasi kestabilan koneksi. Proyek ini juga menjadi media pembelajaran untuk menerapkan pemrograman visual, multithreading, dan integrasi database dalam satu aplikasi desktop.

---

## Daftar Pustaka (Singkat)
1. Dokumentasi Qt for Python (PySide6).
2. Dokumentasi Python: `subprocess`, `socket`, `sqlite3`.
3. Referensi umum tentang ICMP/Ping dan ARP pada jaringan komputer.
