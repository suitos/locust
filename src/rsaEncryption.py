import rsa
import binascii

from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.PublicKey.RSA import construct

def encrypt(modulusvalue, exponent):

    rsa_exponent = int(exponent, 16)
    rsa_modulus = int(modulusvalue, 16)

    password = 'rc5x2013'

    rsa_publickey = rsa.PublicKey(rsa_modulus, rsa_exponent)
    encrypted = rsa.encrypt(password.encode('utf-8'), rsa_publickey)

    #print("Encrypted:", binascii.hexlify(encrypted))

    return str(binascii.hexlify(encrypted)).replace("b'", "").replace("'", "")


def encryptText(exp, pubkey, msg):
    e = int(exp, 16)
    n = int(pubkey, 16)
    keyPub = construct((n, e))

    cipher = Cipher_PKCS1_v1_5.new(keyPub)
    cipher_text = cipher.encrypt(msg.encode())

    emsg = cipher_text.hex()

    return emsg
