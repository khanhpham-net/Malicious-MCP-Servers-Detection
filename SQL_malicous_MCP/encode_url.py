import base64

# Dán link Discord THẬT vào đây
my_real_url = "" 

encoded_bytes = base64.b64encode(my_real_url.encode('utf-8'))
print("CHUỖI BASE64 LÀ:")
print(encoded_bytes.decode('utf-8'))