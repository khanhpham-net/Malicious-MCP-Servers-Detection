import base64

stager_code = """

"""

b64_string = base64.b64encode(stager_code.encode('utf-8')).decode('utf-8')
print("=== COPY CHUỖI BASE64 MỚI DƯỚI ĐÂY ===")
print(b64_string)