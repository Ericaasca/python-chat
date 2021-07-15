import blowfish
import os
import random
import binascii

sharedPrime = 167
sharedBase = 40
iv = b'\x84E\xd0\xd1Kv\x13b'

p_key1 = int(input("Chave publica 1: "))
p_key2 = int(input("Chave publica 2: "))

secret1 = 0
i = 1000
possible_keys1 = []
while i < 30000:
    secret1 = (sharedBase**i) % sharedPrime
    i += 1
    if secret1 == p_key1:
        possible_keys1.append(i)
    
secret2 = 0
j = 1000
possible_keys2 = []
while j < 30000:
    secret2 = (sharedBase**j) % sharedPrime
    j += 1
    if secret2 == p_key2:
        possible_keys2.append(j)

msg_input = input("Mensagem para desencriptar em hexadecimal: ")
msg = bytes.fromhex(msg_input)
keys = []
a = 0
result = ""
while a < len(possible_keys1):
    b = 0
    while b < len(possible_keys2):
        shared_secret1 = (p_key2**a) % sharedPrime
        shared_secret2 = (p_key1**b) % sharedPrime
        if shared_secret1 == shared_secret2:
            if shared_secret1 not in keys:
                keys.append(shared_secret1)
        b += 1
    a += 1
    
for key in keys:
    try:
        aux = key.to_bytes(4, byteorder='big')
        cipher = blowfish.Cipher(aux)
        unencrypted = b"".join(cipher.decrypt_cfb(msg, iv)).decode("utf8")
        print(unencrypted)
    except:
        pass
