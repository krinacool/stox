# payment/RechPayChecksum.py
import hashlib
import base64
from Crypto.Cipher import AES
import json
import random

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

class RechPayChecksum:

    @staticmethod
    def calculate_checksum(params, key, salt):
        hash_string = RechPayChecksum.calculate_hash(params, salt)
        return RechPayChecksum.encrypt(hash_string, key)

    iv = b"@@@@&&&&####$$$$"
    @staticmethod
    def encrypt(input_data, key):
        key = bytes(key, 'utf-8')

        # Initialize the cipher with AES-128-CBC algorithm and the provided key
        cipher = Cipher(algorithms.AES(key), modes.CBC(RechPayChecksum.iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # PKCS7 padding for input data
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(input_data.encode()) + padder.finalize()

        # Encrypt the padded data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Return the Base64-encoded encrypted data
        return base64.b64encode(encrypted_data).decode()



    @staticmethod
    def decrypt(encrypted_data, key):
        key = bytes(key, 'utf-8')

        # Initialize the cipher with AES-128-CBC algorithm and the provided key
        cipher = Cipher(algorithms.AES(key), modes.CBC(RechPayChecksum.iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Base64 decode the input data
        encrypted_data = base64.b64decode(encrypted_data)

        # Decrypt the data
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # PKCS7 unpadding for decrypted data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return unpadded_data.decode()


    @staticmethod
    def generateSignature(params, key):
        if not isinstance(params, (str, list, dict)):
            raise Exception(f"string, list, or dictionary expected, {type(params).__name__} given")

        if isinstance(params, list) or isinstance(params, dict):
            params = RechPayChecksum.get_string_by_params(params)

        return RechPayChecksum.generateSignatureByString(params, key)
    


    @staticmethod
    def verifySignature(params, key, checksum):
        if not isinstance(params, (str, list, dict)):
            raise Exception(f"string, list, or dictionary expected, {type(params).__name__} given")

        if isinstance(params, list) or isinstance(params, dict):
            params = RechPayChecksum.get_string_by_params(params)

        return RechPayChecksum.verifySignatureByString(params, key, checksum)
    

    @staticmethod
    def generateSignatureByString(params, key):
        salt = RechPayChecksum.generate_random_string(4)
        return RechPayChecksum.calculate_checksum(params, key, salt)


    @staticmethod
    def verify_signature_by_string(params, key, checksum):
        rechpay_hash = RechPayChecksum.decrypt(checksum, key)
        salt = rechpay_hash[-4:]
        return rechpay_hash == RechPayChecksum.calculate_hash(params, salt)
    
    @staticmethod
    def generate_random_string(length):
        random.seed()
        data = "9876543210ZYXWVUTSRQPONMLKJIHGFEDCBAabcdefghijklmnopqrstuvwxyz!@#$&_"
        random_string = ''.join(random.choice(data) for _ in range(length))
        return random_string
    
    @staticmethod
    def get_string_by_params(params):
        params = {k: v for k, v in sorted(params.items())}
        params = {k: v if v is not None and v.lower() != "null" else "" for k, v in params.items()}
        return "|".join(params.values())
    
    @staticmethod
    def calculate_hash(params, salt):
        final_string = params + "|" + salt
        hash_obj = hashlib.sha256()
        hash_obj.update(final_string.encode())
        return hash_obj.hexdigest() + salt
    
    
    
    @staticmethod
    def pkcs5_pad(text, blocksize):
        pad = blocksize - (len(text) % blocksize)
        return text + bytes([pad] * pad)
    
    @staticmethod
    def pkcs5_unpad(text):
        pad = text[-1]
        return text[:-pad]
    