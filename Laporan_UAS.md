# Laporan Proyek UAS Praktikum Pemrograman Visual
## Network Scanner & Ping Monitor

**Nama:** [Nama Anda]  
**NIM:** [NIM Anda]  
**Kelas:** [Kelas Anda]  
**Mata Kuliah:** Praktikum Pemrograman Visual  

**Dosen Pengampu:** [Nama Dosen]  
**Tahun Akademik:** [Tahun Akademik]  

---

## Panduan Format (Microsoft Word)
Bagian ini dibuat agar dokumen siap dipindahkan ke Microsoft Word dengan format rapi, daftar isi otomatis, dan penomoran gambar/tabel. Jika sudah selesai format di Word, bagian panduan ini boleh dipertahankan atau dihapus sesuai kebutuhan dosen.

### Pengaturan Halaman (Page Setup)
1. **Ukuran kertas:** A4
2. **Margin (saran umum):** Kiri 4 cm, Kanan 3 cm, Atas 3 cm, Bawah 3 cm (sesuaikan jika kampus punya ketentuan)
3. **Orientasi:** Portrait

### Font dan Spasi
1. **Font:** Times New Roman 12 (atau sesuai pedoman kampus)
2. **Line spacing:** 1.5
3. **Paragraph spacing:** Before 0 pt, After 0–6 pt
4. **Alignment:** Justify (rata kiri-kanan) untuk isi; Center untuk judul

### Heading dan Daftar Isi Otomatis
Agar Word bisa membuat **Daftar Isi otomatis**, pastikan setiap judul bab/subbab memakai Style:
1. Judul bab (contoh: `1. Pendahuluan`) → **Heading 1**
2. Subbab (contoh: `1.1 Latar Belakang`) → **Heading 2**
3. Sub-subbab (jika ada) → **Heading 3**

Cara membuat Daftar Isi:
1. Letakkan kursor di halaman “DAFTAR ISI”
2. Word: **References → Table of Contents → Automatic Table**

### Caption dan Penomoran Gambar/Tabel
Gunakan fitur caption bawaan Word agar nomor otomatis:
1. Klik gambar/tabel → **References → Insert Caption**
2. Label: pilih **Gambar** atau **Tabel**
3. Klik **Numbering…** → centang **Include chapter number** (agar format menjadi `Gambar 5.1`, `Tabel 6.1`, dst.)

### Referensi Silang (Cross Reference)
Untuk merujuk gambar/tabel di isi teks:
1. Word: **References → Cross-reference**
2. Reference type: **Figure**/**Table** → pilih caption → Insert

---

## DAFTAR ISI
(Buat otomatis di Microsoft Word: References → Table of Contents)

---

## Ringkasan
Aplikasi **Network Scanner & Ping Monitor** adalah aplikasi desktop berbasis Python (PySide6) yang digunakan untuk:
1. Melakukan pemindaian rentang IP dan menampilkan status perangkat (Online/Offline/Timeout).
2. Memantau beberapa IP secara berkala (ping monitoring) dengan interval tertentu.
3. Menyimpan riwayat hasil pemindaian ke database SQLite dan menyediakan fitur filter serta ekspor laporan (CSV/Excel).

---

## 1. Pendahuluan

### 1.1 Latar Belakang
Dalam manajemen jaringan, pemantauan perangkat yang terhubung sangat penting untuk memastikan ketersediaan dan keamanan jaringan. Administrator jaringan seringkali membutuhkan alat yang cepat dan mudah digunakan untuk memindai alamat IP dalam suatu rentang tertentu, mengetahui status koneksi (online/offline), serta mendapatkan informasi dasar perangkat seperti Hostname dan MAC Address. Proyek ini bertujuan untuk menyediakan solusi tersebut dalam bentuk aplikasi desktop berbasis GUI.

### 1.2 Tujuan
Tujuan dari proyek ini adalah:
1.  Membuat aplikasi desktop untuk memindai jaringan (Network Scanner).
2.  Mengimplementasikan *multithreading* agar proses scanning berjalan cepat dan tidak membekukan antarmuka pengguna.
3.  Menyediakan fitur logging ke database untuk menyimpan riwayat pemindaian.
4.  Menerapkan pola desain MVC (Model-View-Controller) dalam pengembangan aplikasi.

---

## 2. Deskripsi Proyek

**Network Scanner & Ping Monitor** adalah aplikasi desktop yang dibangun menggunakan bahasa pemrograman Python dan framework PySide6 (Qt for Python). Aplikasi ini memungkinkan pengguna untuk memindai rentang IP, melihat status perangkat, latensi, hostname, MAC address, dan perkiraan sistem operasi.

### 2.1 Fitur Utama
*   **IP Range Scanning:** Memindai rentang IP (misal: 192.168.1.1-254) untuk mendeteksi perangkat aktif.
*   **Ping Monitor:** Mengukur latensi (ping) ke setiap perangkat.
*   **Device Information:** Mendeteksi Hostname, MAC Address, dan perkiraan OS Type.
*   **Database Logging:** Menyimpan hasil scan secara otomatis ke database SQLite (`network_log.db`).
*   **Multithreading:** Menggunakan `QThreadPool` untuk melakukan scanning secara paralel (hingga 50 thread) sehingga proses sangat cepat.
*   **Dark Mode:** Fitur antarmuka untuk mengubah tema menjadi gelap.
*   **Log Viewer + Filter:** Menampilkan riwayat, filter berdasarkan IP, Status, dan Tanggal.
*   **Export Data:** Ekspor log ke **CSV** dan **Excel (.xlsx)**.
*   **Clear History:** Menghapus seluruh riwayat log pada database.

### 2.2 Teknologi yang Digunakan
*   **Bahasa Pemrograman:** Python 3.x
*   **GUI Framework:** PySide6 (Qt)
*   **Database:** SQLite3
*   **Library Ekspor Excel:** openpyxl
*   **System Libraries:** `subprocess` (ping), `socket` (hostname/DNS reverse), `threading` (lock DB), `re` (regex parsing).

---

## 3. Analisis Kebutuhan

### 3.1 Kebutuhan Fungsional
1. Sistem menerima input rentang IP dengan format `A.B.C.D-X` (contoh: `192.168.1.1-254`).
2. Sistem melakukan ping untuk setiap IP dalam rentang dan menentukan status:
    - **Online** jika ping berhasil.
    - **Offline** jika ping gagal.
    - **Timeout** jika proses ping melebihi batas waktu.
3. Sistem menampilkan hasil scan pada tabel: IP, Hostname, MAC Address, OS Type, Status, Latency.
4. Sistem dapat memonitor beberapa IP (daftar monitoring) dengan interval 1–300 detik.
5. Sistem menyimpan hasil scan ke database SQLite dan dapat menampilkan log.
6. Sistem menyediakan filter log (IP, status, tanggal), ekspor log (CSV/Excel), dan hapus riwayat.
7. Sistem menyediakan mode tema gelap (dark mode).

### 3.2 Kebutuhan Non-Fungsional
1. **Responsif:** Proses scan berjalan tanpa membekukan UI.
2. **Kinerja:** Pemindaian dilakukan paralel menggunakan thread pool (maksimum 50 thread).
3. **Portabilitas:** Kompatibel Windows (utama) dan tetap mempertimbangkan Linux/Mac pada argumen ping.
4. **Keandalan:** Penulisan database thread-safe menggunakan mekanisme lock.
5. **Usability:** Tersedia tab terpisah untuk Scanner, Ping Monitor, dan Log Viewer.

---

## 4. Arsitektur Sistem

Proyek ini disusun menggunakan pendekatan modular yang memisahkan logika bisnis, data, dan antarmuka pengguna (mirip dengan pola MVC).

### 4.1 Struktur Folder
```
Project_UAS/
├── main.py                 # Entry point aplikasi
├── config/                 # Konfigurasi dan konstanta
├── controllers/            # Logika pemindaian (Scanner)
│   └── scanner.py
├── models/                 # Manajemen Database
│   └── database.py
├── ui/                     # Antarmuka Pengguna (GUI)
│   └── main_window.py
└── requirements.txt        # Daftar dependensi
```

### 4.2 Penjelasan Modul
1.  **Models (`models/database.py`):**
    *   Bertanggung jawab atas semua operasi database.
    *   Menggunakan SQLite untuk menyimpan data hasil scan (`log_network`).
    *   Memiliki fitur *thread-safety* menggunakan `threading.Lock` untuk mencegah konflik saat penulisan data dari banyak thread.

2.  **Controllers (`controllers/scanner.py`):**
    *   Berisi logika inti pemindaian.
    *   `ScanWorker` (turunan `QRunnable`): Melakukan ping ke satu IP dalam thread terpisah.
    *   Menggunakan perintah sistem (`ping`) melalui `subprocess` untuk kompatibilitas lintas platform (Windows/Linux/Mac).

3.  **Views/UI (`ui/main_window.py`):**
    *   Menangani tampilan utama aplikasi menggunakan `QMainWindow`.
    *   Mengelola input pengguna, tombol, tabel hasil, dan progress bar.
    *   Menghubungkan interaksi pengguna dengan logic di controller.

---

## 5. Perancangan (Desain Sistem)

### 5.1 Use Case (Ringkas)
**Aktor:** User

Use case utama:
1. Melakukan scan IP range.
2. Melihat hasil scan pada tabel.
3. Menambahkan IP ke daftar monitoring.
4. Menjalankan/berhenti monitoring periodik.
5. Melihat log hasil scan.
6. Memfilter log (IP/status/tanggal).
7. Ekspor log ke CSV/Excel.
8. Menghapus seluruh riwayat log.

### 5.2 Alur Proses Scan (Flow)
1. User memasukkan IP range pada tab **Scanner**.
2. Sistem memvalidasi format IP range.
3. Sistem membuat tugas scan per-IP menggunakan `ScanWorker`.
4. `QThreadPool` mengeksekusi tugas secara paralel.
5. Tiap worker mengirim hasil melalui signal ke UI.
6. UI menambahkan baris ke tabel hasil dan memperbarui progress.
7. Hasil scan disimpan ke database (untuk log histori).

### 5.3 Desain Antarmuka (UI)
Aplikasi memiliki 3 tab utama:
1. **Scanner**: input IP range, tombol start/stop scan, progress bar, tabel hasil, dan status.
2. **Ping Monitor**: input IP & interval, daftar monitoring, tombol start/stop monitoring, dan tabel monitoring.
3. **Log Viewer**: filter log (IP/status/tanggal), tombol clear filters, export CSV/Excel, clear history, serta tabel log.

Catatan dokumentasi:
- Untuk laporan cetak, tambahkan screenshot: (1) Tab Scanner saat scan, (2) Tab Ping Monitor, (3) Tab Log Viewer + filter, (4) Dark mode.

Template caption (pakai Insert Caption di Word):
- Gambar 5.1 Tampilan Tab Scanner
- Gambar 5.2 Proses scanning dan progress bar
- Gambar 5.3 Tampilan Tab Ping Monitor
- Gambar 5.4 Tampilan Tab Log Viewer dan filter

---

## 6. Implementasi Kode

Berikut adalah beberapa bagian penting dari implementasi kode:

### 6.1 Multithreading Scanning (`controllers/scanner.py`)
Aplikasi menggunakan `QThreadPool` untuk menjalankan banyak instance `ScanWorker` secara bersamaan. Ini sangat meningkatkan kecepatan scanning dibandingkan proses sekuensial.

```python
class ScanWorker(QRunnable):
    def run(self):
        # ... setup command ping sesuai OS ...
        process = subprocess.run(command, ...)
        
        if process.returncode == 0:
            # Jika host online, ambil info tambahan
            latency = self._get_latency(process.stdout)
            hostname = self._get_hostname_fast(self.ip)
            # ... emit signal result ...
```

Penjelasan:
- Aplikasi menggunakan `QThreadPool` dan `QRunnable` agar proses ping berjalan paralel.
- Untuk Windows, proses ping dijalankan tanpa membuka jendela console (`subprocess.CREATE_NO_WINDOW`).
- Timeout dibuat pendek agar scanning tidak terlalu lama (misal `-w 500` ms pada Windows dan `timeout=2`).

### 6.2 Deteksi OS (TTL-based)
Pada hasil ping, aplikasi mengambil nilai TTL untuk perkiraan tipe OS:
- TTL ≥ 128 → cenderung **Windows**
- TTL ≥ 64 → cenderung **Linux/Unix**
- TTL ≥ 32 → **Windows (Routed)**

Keterbatasan: TTL bukan identifikasi OS yang pasti, tetapi perkiraan berdasarkan nilai umum.

### 6.3 Pengambilan MAC Address (ARP Cache)
Setelah ping berhasil, aplikasi mencoba mengambil MAC Address dari ARP cache:
- Windows: `arp -a <ip>`
- Linux/Mac: `arp -n <ip>`

Jika MAC tidak ditemukan, nilai default ditampilkan sebagai `-`.

### 6.4 Database Handling (`models/database.py`)
Penyimpanan data dilakukan dengan aman menggunakan locking mechanism.

```python
def insert_log(self, ip, hostname, status, latency, ...):
    with self.lock:  # Mencegah race condition
        conn = self._get_connection()
        # ... execute INSERT query ...
        conn.commit()
```

**Skema tabel `log_network`:**
- `id` (INTEGER, PK, AUTOINCREMENT)
- `ip_address` (TEXT)
- `hostname` (TEXT)
- `mac_address` (TEXT)
- `os_type` (TEXT)
- `status` (TEXT)
- `latency` (TEXT)
- `timestamp` (TEXT)

**Catatan migrasi:**
Terdapat fungsi `_migrate_database()` yang menambahkan kolom `os_type` jika database lama belum memilikinya.

### 6.5 Main Window Logic (`ui/main_window.py`)
Menginisialisasi thread pool dan menangani hasil scan yang dikirim oleh worker.

```python
self.thread_pool = QThreadPool()
self.thread_pool.setMaxThreadCount(50)  # Maksimum 50 thread paralel

# Saat tombol scan ditekan
worker = ScanWorker(ip, self.scan_session_id)
worker.signals.result.connect(self.handle_scan_result)
self.thread_pool.start(worker)
```

Selain tab Scanner, UI juga menyediakan:
- Tab **Ping Monitor**: daftar IP yang dipantau berkala dengan interval 1–300 detik.
- Tab **Log Viewer**: filter log (IP/status/tanggal), ekspor CSV/Excel, dan clear history.

### 6.6 Validasi dan Parsing IP Range
Pada saat user menekan **Start Scan**, aplikasi melakukan validasi input menggunakan regex, lalu memecah IP menjadi tiga oktet awal dan rentang host.

Aturan yang diterapkan:
- Format yang didukung: **Single IP** (`192.168.1.1`) atau **Range** (`192.168.1.1-254`).
- Validasi tiap oktet berada pada rentang 0–255.
- Jika range diberikan, maka `start <= end` dan `end <= 255`.
- Jika jumlah IP terlalu besar (lebih dari 254), aplikasi menampilkan konfirmasi (*Large Scan Warning*) sebelum melanjutkan.

### 6.7 Pengolahan Hasil Scan (Session ID + UI Responsif)
Hasil dari `ScanWorker` membawa `session_id`. UI mengabaikan hasil dari sesi scan yang sudah tidak aktif (misalnya setelah tombol **Stop Scan** ditekan), sehingga data yang masuk tetap konsisten.

Catatan implementasi penting:
- Tabel hasil pada tab **Scanner** hanya menampilkan perangkat dengan status **Online**.
- Walaupun tabel hanya menampilkan Online, hasil scan (Online/Offline/Timeout) tetap dicatat ke database.

### 6.8 Log Viewer, Filter, dan Ekspor
Tab **Log Viewer** menampilkan data dari database dan menyediakan:
- Filter IP (partial match / `LIKE`), filter status, dan filter tanggal.
- Ekspor CSV menggunakan modul `csv`.
- Ekspor Excel menggunakan `openpyxl`, dengan header diberi style (bold + warna).

Catatan implementasi:
- Query log pada aplikasi memfilter hostname agar bukan `'-'` dan bukan string kosong, sehingga log yang ditampilkan umumnya perangkat yang memiliki hostname valid.
- Ekspor CSV/Excel mengekspor isi tabel log yang sedang tampil (sudah terpengaruh filter).

### 6.9 Clear History
Fitur **Clear History** menampilkan dialog konfirmasi dan kemudian menjalankan penghapusan seluruh record pada tabel `log_network` di SQLite.

---

## 7. Cara Instalasi dan Menjalankan Program

### 7.1 Persiapan Environment
1. Pastikan Python 3.x sudah ter-install.
2. Install dependensi:

```bash
pip install -r requirements.txt
```

### 7.2 Menjalankan Aplikasi (Mode Development)
Jalankan:

```bash
python main.py
```

### 7.3 Cara Penggunaan (Singkat)
1. Buka tab **Scanner** → masukkan IP range contoh `192.168.1.1-254` → klik **Start Scan**.
2. Untuk monitoring → tab **Ping Monitor** → isi IP dan interval → **Add to Monitor** → **Start Monitoring**.
3. Lihat histori → tab **Log Viewer** → gunakan filter atau ekspor.

---

## 8. Pengujian

### 8.1 Skenario Uji Fungsional
1. **Validasi IP Range**
    - Input valid: `192.168.1.1-254` → scan berjalan.
    - Input invalid: format salah → aplikasi menolak dan menampilkan pesan error.
2. **Scan Online/Offline**
    - IP aktif → status Online dan latency terbaca.
    - IP tidak aktif → status Offline.
    - Kondisi jaringan lambat → status Timeout.
3. **Monitoring**
    - Tambah beberapa IP → tabel monitoring terisi.
    - Start monitoring → last check ter-update berkala sesuai interval.
4. **Log Viewer**
    - Setelah scan, log bertambah.
    - Filter IP/status/tanggal berfungsi.
    - Export CSV/Excel menghasilkan file.
    - Clear history menghapus data log.

### 8.2 Pengujian Kinerja (Observasi)
Dengan `QThreadPool` maksimum 50 thread, scanning pada satu segmen /24 (hingga 254 host) dapat diselesaikan lebih cepat dibanding metode sekuensial, dengan tetap menjaga UI responsif.

---

## 9. Packaging (Distribusi Aplikasi)

Proyek menyediakan file spec PyInstaller: `NetworkScanner.spec`.

### 9.1 Build dengan PyInstaller
Contoh perintah build:

```bash
pyinstaller NetworkScanner.spec
```

Konfigurasi penting:
- Output bernama `NetworkScanner`
- Mode windowed (`console=False`) sehingga tidak menampilkan terminal saat aplikasi dijalankan.

---

## 10. Keterbatasan dan Saran Pengembangan

### 10.1 Keterbatasan
1. Deteksi OS berbasis TTL adalah perkiraan, bukan identifikasi pasti.
2. MAC Address bergantung pada ARP cache; beberapa kondisi jaringan/perangkat dapat membuat MAC tidak muncul.
3. Hasil hostname bergantung pada reverse DNS; jika tidak tersedia akan tampil `-`.

### 10.2 Saran Pengembangan
1. Menambahkan penyimpanan konfigurasi (misal default IP range, interval monitoring).
2. Menambahkan export format tambahan (PDF) atau template laporan.
3. Menambahkan ringkasan statistik (jumlah online/offline per sesi scan).

---

## 11. Daftar Pustaka
1. Qt for Python (PySide6) Documentation.
2. Python Standard Library Documentation: `subprocess`, `socket`, `sqlite3`.
3. openpyxl Documentation (export Excel).

---

## 12. Kesimpulan

Proyek **Network Scanner & Ping Monitor** ini berhasil diimplementasikan sebagai aplikasi desktop yang fungsional. Penggunaan PySide6 memberikan antarmuka yang responsif dan modern, sementara implementasi *multithreading* memastikan kinerja scanning yang efisien. Struktur kode yang terorganisir memudahkan pemeliharaan dan pengembangan fitur lebih lanjut di masa depan.

Aplikasi ini memenuhi kebutuhan dasar administrator jaringan untuk pemantauan cepat dan pencatatan aktivitas perangkat dalam jaringan lokal.
