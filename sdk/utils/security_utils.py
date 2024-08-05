import base64
import hashlib
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class SecurityUtils:

    @staticmethod
    def generate_iv():
        return os.urandom(16)

    @staticmethod
    def base64_encode(byte_array):
        encoded_bytes = base64.b64encode(byte_array)
        return encoded_bytes.decode('utf-8')

    @staticmethod
    def cbc_encryption(data, key, iv, encrypt=True):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        if encrypt:
            encrypted_data = cipher.encrypt(pad(data, AES.block_size))
            return encrypted_data
        else:
            decrypted_data = unpad(cipher.decrypt(data), AES.block_size)
            return decrypted_data

    @staticmethod
    def hash256(data):
        try:
            message_digest = hashlib.sha256()
            message_digest.update(data)
            return message_digest.digest()
        except Exception as e:
            print(e)
            return None
