import hashlib
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def pad(m):
    return m+(chr(16-len(m)%16)*(16-len(m)%16)).encode()

def unpad(s):
    return s[:-ord(s[len(s)-1:])]

"""
    Takes in a hash in bytes and an input password to check whether or not that
    password-salt str-byte pair would generate a key which its hash matches the check hash
"""
def verifyKeyHash(check: bytes, input: str, salt: bytes) -> bool:
    possible = regenerateKey(input, salt)
    possible = hashlib.sha256((possible+salt)).digest()
    if (possible == check):
        return True
    return False

"""
   Takes in a password as a string and a salt of 16 bytes or longer to 
   generate a 256 bit key based off of the inputted password
"""
def regenerateKey(password: str, salt: bytes):

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1200000,
    )
    key = kdf.derive(password.encode("utf-8"))
    return key

"""
    Takes in a key and plaintext and returns a ciphertext in base64
    TODO: ensure IV is always different
"""
def encrypt(key: bytes, plaintext: str):
    plaintext = pad(plaintext.encode("utf-8"))
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    msg = encryptor.update(plaintext) + encryptor.finalize()
    return base64.b64encode(iv + msg)

"""
    takes in a key and ciphertext and returns a byte string of the plaintext
"""
def decrypt(key: bytes, ciphertext: str):
    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    return unpad(decryptor.update(ciphertext[16:]) + decryptor.finalize())




    
