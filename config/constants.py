#Constants buatan aplikasi Network Scanner & Ping Monitor
#Fungsi: Menyimpan nilai konfigurasi terpusat untuk menghindari angka ajaib dan string yang di-hardcode
#Agar kode lebih mudah dipelihara dan dibaca oleh pengembang lainnya.
# Application Information
APP_TITLE = "Network Scanner & Ping Monitor"
APP_VERSION = "1.0.0"

#Setelan Jendela Utama
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_X = 100
WINDOW_Y = 100

#Dimensi UI
BUTTON_HEIGHT = 30
DARK_MODE_BUTTON_WIDTH = 130
SCAN_BUTTON_WIDTH = 120
MONITOR_BUTTON_WIDTH = 120
START_MONITOR_BUTTON_WIDTH = 130
REMOVE_MONITOR_BUTTON_WIDTH = 150
FILTER_BUTTON_WIDTH = 100
EXPORT_BUTTON_WIDTH = 140

INPUT_MAX_WIDTH = 150
INTERVAL_INPUT_WIDTH = 70
DATE_INPUT_WIDTH = 120

PROGRESS_BAR_HEIGHT = 20

#Spacing buat Layout
LAYOUT_MARGIN = 10
LAYOUT_SPACING = 5
HEADER_SPACING = 10
SECTION_SPACING = 8

#Config Jaringan
SOCKET_TIMEOUT = 2  # seconds
PING_COUNT = 1
PING_TIMEOUT_MS = 1000  # milliseconds for Windows
PING_TIMEOUT_SEC = 1  # seconds for Linux/Mac
SUBPROCESS_TIMEOUT = 3  # seconds
ARP_WAIT_TIME = 0.1  # seconds - wait for ARP table update
ARP_TIMEOUT = 2  # seconds

#Validasi IP
MAX_OCTET_VALUE = 255
MIN_OCTET_VALUE = 0
MAX_IP_SCAN_WARNING = 254  #Peringatan kalau scan lebih dari 254 IP

#Setelan Threading
THREAD_SHUTDOWN_TIMEOUT = 3000  # milliseconds - max wait for threads to finish

#Setelan Monitor
MIN_MONITOR_INTERVAL = 1  # seconds
MAX_MONITOR_INTERVAL = 300  # seconds
DEFAULT_MONITOR_INTERVAL = 5  # seconds
LOG_REFRESH_THROTTLE = 2  # seconds - minimum time between log refreshes

#Pesan Status
MSG_READY = "Ready"
MSG_SCANNING = "Scanning {} IP addresses..."
MSG_SCAN_COMPLETE = "Scan completed! Found {} online device(s) from {} scanned"
MSG_SCAN_STOPPED = "Scan stopped"
MSG_SCAN_CANCELLED = "Scan cancelled"
MSG_NOT_MONITORING = "Not monitoring"
MSG_MONITORING = "Monitoring {} IP(s) every {}s"
MSG_MONITORING_STOPPED = "Monitoring stopped"

#Pesan Error
ERR_NO_IP_RANGE = "Error: Please enter IP range"
ERR_INVALID_IP_FORMAT = "Error: Invalid IP format"
ERR_INVALID_OCTET = "Error: Invalid IP octet value"
ERR_INVALID_RANGE = "Error: Invalid range"
ERR_INVALID_RANGE_END = "Error: Invalid range end value"
ERR_ENTER_IP = "Error: Enter IP address"

# Judul Dialog
TITLE_INPUT_ERROR = "Input Error"
TITLE_INVALID_FORMAT = "Invalid Format"
TITLE_INVALID_IP = "Invalid IP"
TITLE_INVALID_RANGE = "Invalid Range"
TITLE_PARSE_ERROR = "Parsing Error"
TITLE_UNEXPECTED_ERROR = "Unexpected Error"
TITLE_LARGE_SCAN_WARNING = "Large Scan Warning"
TITLE_SUCCESS = "Success"
TITLE_ERROR = "Error"
TITLE_MODULE_NOT_FOUND = "Module Not Found"
TITLE_NO_SELECTION = "No Selection"
TITLE_ALREADY_IN_MONITOR = "Already in Monitor"
TITLE_ADDED_TO_MONITOR = "Added to Monitor"
TITLE_BATCH_ADD_COMPLETE = "Batch Add Complete"

#Bagian Header Tabel
HEADERS_SCANNER = ["IP Address", "Hostname", "MAC Address", "OS Type", "Status", "Latency"]
HEADERS_MONITOR = ["IP Address", "Hostname", "MAC Address", "Status", "Latency", "Last Check"]
HEADERS_LOG = ["Timestamp", "IP Address", "Hostname", "MAC Address", "OS Type", "Status", "Latency"]

#Nilai Status
STATUS_ONLINE = "Online"
STATUS_OFFLINE = "Offline"
STATUS_TIMEOUT = "Timeout"
STATUS_WAITING = "Waiting..."
STATUS_UNKNOWN = "-"

#Ekstensi File Export
EXT_CSV = "CSV Files (*.csv)"
EXT_EXCEL = "Excel Files (*.xlsx)"

#Nama File secara bawaan
FILE_CSV_DEFAULT = "network_log.csv"
FILE_EXCEL_DEFAULT = "network_log.xlsx"
FILE_DATABASE = "network_log.db"

#Warna (RGB)
COLOR_DARK_WINDOW = (53, 53, 53)
COLOR_DARK_BASE = (35, 35, 35)
COLOR_DARK_ALTERNATE = (53, 53, 53)
COLOR_DARK_BUTTON = (53, 53, 53)
COLOR_OFFLINE_BG = (255, 200, 200)

#Ekspresi Reguler
REGEX_IP_PATTERN = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})(?:-(\d{1,3}))?$'
REGEX_MAC_ADDRESS = r'([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}'
REGEX_TTL = r'[Tt][Tt][Ll][=:](\d+)'
REGEX_LATENCY = r'[Tt]ime[=<](\d+)ms'

#Teks Template/Contoh
PLACEHOLDER_IP_RANGE = "192.168.1.x-xxx"
PLACEHOLDER_MONITOR_IP = "192.168.1.x"
PLACEHOLDER_FILTER_IP = "e.g., 192.168.1"

#Nama Tab
TAB_SCANNER = "Scanner"
TAB_MONITOR = "Ping Monitor"
TAB_LOG = "Log Viewer"

#Label Tombol
BTN_DARK_MODE = "🌙 Dark Mode"
BTN_LIGHT_MODE = "☀️ Light Mode"
BTN_START_SCAN = "Start Scan"
BTN_STOP_SCAN = "Stop Scan"
BTN_START_MONITORING = "Start Monitoring"
BTN_STOP_MONITORING = "Stop Monitoring"
BTN_ADD_TO_MONITOR = "Add to Monitor"
BTN_REMOVE_FROM_MONITOR = "Remove from Monitor"
BTN_CLEAR_FILTERS = "Clear Filters"
BTN_EXPORT_CSV = "📄 Export to CSV"
BTN_EXPORT_EXCEL = "📊 Export to Excel"

#Label Konteks Menu
MENU_SELECT_ALL = "✅ Select All (Ctrl+A)"
MENU_ADD_TO_MONITOR = "➕ Add to Ping Monitor"
MENU_ADD_ALL_TO_MONITOR = "➕ Add All ({}) to Ping Monitor"
MENU_REMOVE_FROM_MONITOR = "🗑️ Remove All ({}) from Monitor"
MENU_COPY = "📋 Copy"
MENU_COPY_ALL_IPS = "📋 Copy All ({}) IP Addresses"

#Deteksi Sistem Operasi berdasarkan TTL
TTL_CISCO = 240
TTL_WINDOWS = 128
TTL_WINDOWS_ROUTED = 100
TTL_LINUX = 64
TTL_LINUX_ROUTED = 60
TTL_WINDOWS_MULTIHOP = 32

OS_CISCO = "Cisco/Network"
OS_WINDOWS = "Windows"
OS_WINDOWS_ROUTED = "Windows (Routed)"
OS_LINUX = "Linux/Unix"
OS_LINUX_ROUTED = "Linux/Unix (Routed)"
OS_WINDOWS_MULTIHOP = "Windows (Multi-hop)"
OS_LEGACY = "Legacy/Embedded"
OS_UNKNOWN = "-"

#Opsi Buat Filter
FILTER_ALL = "All"
FILTER_ONLINE = "Online"
FILTER_OFFLINE = "Offline"
FILTER_ALL_DATES = "All Dates"

#Durasi Notifikasi
NOTIFICATION_DURATION = 2000  # milliseconds(2 detik)

#Setelan Ekspor Excel
EXCEL_HEADER_COLOR = "4472C4"
EXCEL_FONT_COLOR = "FFFFFF"
EXCEL_COLUMN_PADDING = 2
