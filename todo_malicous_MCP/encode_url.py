import base64

# Dán link Discord THẬT của mày vào đây
my_real_url = "" 

encoded_bytes = base64.b64encode(my_real_url.encode('utf-8'))
print("CHUỖI BASE64 CỦA MÀY LÀ:")
print(encoded_bytes.decode('utf-8'))