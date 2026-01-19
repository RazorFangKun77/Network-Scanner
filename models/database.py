import sqlite3#Import sqlite3 untuk database
from datetime import datetime#Import datetime untuk timestamp
import threading#Import threading untuk thread safety(biar aman diakses banyak thread)


class Database:
    def __init__(self, db_name="network_log.db"):
        self.db_name = db_name
        self.lock = threading.Lock()  #Tambahkan lock untuk thread safety
        self._init_connection()
#Inisialisasi koneksi database dan buat tabel jika belum ada
    def _init_connection(self):
        """Initialize database connection and create table"""
        #Buat koneksi tanpa check_same_thread=False
        conn = sqlite3.connect(self.db_name)
        self._create_table(conn)
        self._migrate_database(conn)  #Tambahkan migration untuk update schema
        conn.close()
#Buat tabel log_network jika belum ada
    def _create_table(self, conn):
        """Create table if not exists"""
        query = """
        CREATE TABLE IF NOT EXISTS log_network (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            hostname TEXT,
            mac_address TEXT,
            os_type TEXT,
            status TEXT,
            latency TEXT,
            timestamp TEXT
        )
        """
        conn.execute(query)
        conn.commit()
    #Migrasi database untuk menambahkan kolom os_type jika belum ada
    def _migrate_database(self, conn):
        """Migrate database schema - add missing columns if needed"""
        try:
            cursor = conn.cursor()
            
            #Cek kalau kolom os_type sudah ada/belum
            cursor.execute("PRAGMA table_info(log_network)")
            columns = [column[1] for column in cursor.fetchall()]
            
            #Tambahkan kolom os_type jika belum ada
            if 'os_type' not in columns:
                cursor.execute("ALTER TABLE log_network ADD COLUMN os_type TEXT DEFAULT '-'")
                conn.commit()
                print("✓ Database migrated: Added 'os_type' column")
        except Exception as e:
            print(f"Migration check: {str(e)}")
            pass
#Dapatkan koneksi baru untuk setiap operasi(biar thread-safe)
    def _get_connection(self):
        """Get a new connection for each operation (thread-safe)"""
        return sqlite3.connect(self.db_name)
#Sisipkan log baru dengan thread safety
    def insert_log(self, ip, hostname, status, latency, mac_address="-", os_type="-"):
        """Insert log with thread safety using lock"""
        with self.lock:  # Gunakan lock untuk mencegah race condition
            conn = self._get_connection()
            try:
                query = """
                INSERT INTO log_network
                (ip_address, hostname, mac_address, os_type, status, latency, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                conn.execute(
                    query,
                    (ip, hostname, mac_address, os_type, status, latency, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                conn.commit()
            finally:
                conn.close()
#Ambil semua log dari database
    def fetch_logs(self):
        """Fetch all logs"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT timestamp, ip_address, hostname, mac_address, os_type, status, latency
                FROM log_network
                ORDER BY id DESC
            """)
            return cursor.fetchall()
        finally:
            conn.close()
#Ambil log dengan hostname valid(sesuai kriteria)
    def fetch_logs_with_hostname(self):
        """Fetch only logs with valid hostname (not '-' or empty)"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT timestamp, ip_address, hostname, mac_address, os_type, status, latency
                FROM log_network
                WHERE hostname IS NOT NULL 
                AND hostname != '-' 
                AND hostname != ''
                ORDER BY id DESC
            """)
            return cursor.fetchall()
        finally:
            conn.close()
#Ambil log dengan filter tertentu
    def fetch_logs_filtered(self, ip_filter="", status_filter="", date_filter=""):
        """Fetch logs with filters"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            #Buat query dasar
            query = """
                SELECT timestamp, ip_address, hostname, mac_address, os_type, status, latency
                FROM log_network
                WHERE hostname IS NOT NULL 
                AND hostname != '-' 
                AND hostname != ''
            """
            
            params = []
            #Tambahkan filter IP jika ada
            if ip_filter:
                query += " AND ip_address LIKE ?"
                params.append(f"%{ip_filter}%")
            #Tambahkan filter status jika ada
            if status_filter and status_filter != "All":
                query += " AND status = ?"
                params.append(status_filter)
            #Tambahkan filter tanggal jika ada
            if date_filter:
                query += " AND DATE(timestamp) = ?"
                params.append(date_filter)
            #Urutkan hasil berdasarkan ID descending
            query += " ORDER BY id DESC"
            #Eksekusi query dengan parameter
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            conn.close()
#Tutup koneksi database (tidak ada koneksi persisten lagi)
    def close(self):
        """Close method for compatibility (no persistent connection anymore)"""
        pass
#Hapus semua log dari database dengan thread safety    
    def clear_all_logs(self):
        """Clear all logs from database"""
        with self.lock:
            conn = self._get_connection()
            try:
                conn.execute("DELETE FROM log_network")
                conn.commit()
                return True
            except Exception as e:
                print(f"Error clearing logs: {str(e)}")
                return False
            finally:
                conn.close()
