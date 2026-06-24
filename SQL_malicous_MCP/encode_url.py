import base64

# Dán link Discord THẬT của mày vào đây
my_real_url = "https://discord.com/api/webhooks/1504104476414443662/iOE1r0kzTTFodUK9A8FIDNXp9Lg2OrAIlhYjRk_Pwto8Oldo1QcF5uA20jLmyzSy_Tiq" 

encoded_bytes = base64.b64encode(my_real_url.encode('utf-8'))
print("CHUỖI BASE64 CỦA MÀY LÀ:")
print(encoded_bytes.decode('utf-8'))