import socket# Untuk operasi socket dengan timeout
import subprocess# Untuk menjalankan perintah ping dan arp
import re# Untuk parsing output
import platform# Untuk mendeteksi OS sistem operasi
from PySide6.QtCore import QObject, Signal, QRunnable# Untuk threading dengan sinyal

#Set default timeout untuk socket operations (lebih pendek)
socket.setdefaulttimeout(1)
#Struktur data untuk hasil scan
class ScanResult:
    def __init__(self, ip, hostname, status, latency, mac_address="", os_type="-", session_id=0):
        self.ip = ip
        self.hostname = hostname
        self.status = status
        self.latency = latency
        self.mac_address = mac_address
        self.os_type = os_type
        self.session_id = session_id  # Tambahkan session_id ke result

#Worker untuk melakukan scan ping
class ScanWorkerSignals(QObject):
    result = Signal(object)

#Worker QRunnable untuk scan ping
class ScanWorker(QRunnable):
    def __init__(self, ip, session_id=0):
        super().__init__()
        self.ip = ip
        self.session_id = session_id  # Simpan session_id
        self.signals = ScanWorkerSignals()
        self.setAutoDelete(True)
#Jalankan scan ping
    def run(self):
        try:
            #Deteksi OS untuk menentukan perintah ping yang sesuai
            system_os = platform.system().lower()
            
            #Buat subprocess flags untuk Windows (no window)
            creationflags = 0
            if system_os == "windows":
                creationflags = subprocess.CREATE_NO_WINDOW
                # Windows: -n count, -w timeout (ms) - timeout lebih pendek
                command = ["ping", "-n", "1", "-w", "500", self.ip]
            else:
                # Linux/Mac: -c count, -W timeout (seconds)
                command = ["ping", "-c", "1", "-W", "1", self.ip]

            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=2,  #Timeout lebih pendek biar responsif
                creationflags=creationflags
            )

            if process.returncode == 0:
                latency = self._get_latency(process.stdout)
                os_type = self._detect_os(process.stdout)
                
                # Get MAC Address dari ARP cache (tanpa delay)
                mac_address = self._get_mac_address(self.ip)
                
                # Get hostname - gunakan cara cepat saja
                hostname = self._get_hostname_fast(self.ip)
                
                result = ScanResult(self.ip, hostname, "Online", latency, mac_address, os_type, self.session_id)
            else:
                result = ScanResult(self.ip, "-", "Offline", "-", "-", "-", self.session_id)

            self.signals.result.emit(result)

        except subprocess.TimeoutExpired:
            #Ping timeout
            self.signals.result.emit(
                ScanResult(self.ip, "-", "Timeout", "-", "-", "-", self.session_id)
            )
        except Exception as e:
            #Emit Offline untuk error agar scan tetap lanjut
            self.signals.result.emit(
                ScanResult(self.ip, "-", "Offline", "-", "-", "-", self.session_id)
            )
    # Mendapatkan hostname dengan cara cepat
    def _get_hostname_fast(self, ip):
        """Get hostname dengan cara cepat - hanya DNS lookup"""
        try:
            #Hanya gunakan DNS lookup dengan timeout pendek
            old_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(0.5)  # 500ms timeout
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                if hostname and hostname != ip:
                    return hostname
            finally:
                socket.setdefaulttimeout(old_timeout)
        except:
            pass
        
        return "-"
#Ekstrak latency dari output ping
    def _get_latency(self, output):
        """Extract latency dengan pattern yang lebih luas"""
        for line in output.splitlines():
            # Windows/Linux format: time=123ms or time<1ms
            if "time=" in line.lower() or "time<" in line.lower():
                try:
                    # Pattern 1: time=123ms or Time=123ms
                    match = re.search(r'[Tt]ime[=<](\d+)ms', line)
                    if match:
                        return f"{match.group(1)} ms"
                    
                    # Pattern 2: time<1ms
                    if "time<1ms" in line.lower():
                        return "<1 ms"
                    
                    # Pattern 3: time = 123 ms (with spaces)
                    match = re.search(r'[Tt]ime\s*[=<]\s*(\d+)\s*ms', line)
                    if match:
                        return f"{match.group(1)} ms"
                except:
                    pass
        
        return "-"
   #Dapatkan MAC address dari ARP cache 
    def _get_mac_address(self, ip):
        """Get MAC address dari ARP cache - cepat karena sudah ada di cache"""
        try:
            system_os = platform.system().lower()
            creationflags = 0
            
            if system_os == "windows":
                creationflags = subprocess.CREATE_NO_WINDOW
                # Windows: arp -a dengan IP spesifik lebih cepat
                command = ["arp", "-a", ip]
            else:
                # Linux/Mac: arp -n
                command = ["arp", "-n", ip]
            
            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=1,  #Timeout sangat pendek karena lokal
                creationflags=creationflags
            )
            
            if process.returncode == 0:
                output = process.stdout
                
                #ngeparse output untuk cari MAC address dari ARP cache
                for line in output.splitlines():
                    if ip in line:
                        #Ekstrak MAC address dengan regex
                        match = re.search(r'([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}', line)
                        if match:
                            mac = match.group(0)
                            mac_normalized = mac.upper().replace('-', ':')
                            
                            if mac_normalized not in ["FF:FF:FF:FF:FF:FF", "00:00:00:00:00:00"]:
                                return mac_normalized
            
            return "-"
        except Exception:
            return "-"
#Deteksi OS berdasarkan nilai TTL dari respons ping
    def _detect_os(self, output):
        """Detect OS based on TTL value from ping response"""
        try:
            match = re.search(r'[Tt][Tt][Ll][=:](\d+)', output)
            
            if match:
                ttl = int(match.group(1))
                
                if ttl >= 128:#Windows default TTL
                    return "Windows"
                elif ttl >= 64:#Linux/Unix(Android) default TTL
                    return "Linux/Unix"
                elif ttl >= 32:#Cisco default TTL
                    return "Windows (Routed)"
                else:
                    return "Unknown"
            
            return "-"
        except Exception:
            return "-"
