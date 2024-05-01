from Crypto.Cipher import AES

key = b"lolamento2345678"
iv = b"1234567890123456"

def encrypt(data):
	l = len(data)
	if l%16 != 0:
		for x in range(l%16, 16):
			data += ' '
	obj = AES.new(key, AES.MODE_CBC, iv)
	enc = obj.encrypt(data.encode())
	return enc.hex()

def decrypt(data):
	obj = AES.new(key, AES.MODE_CBC, iv)
	decd = obj.decrypt(bytes.fromhex(data))
	return decd.decode("utf-8").strip()
