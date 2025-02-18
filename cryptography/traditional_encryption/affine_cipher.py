from cipher_utils import *

import math

KEY = 113


def is_prime(x: int) -> bool:
    for i in range(2, int(math.sqrt(x)+1)):
        if x % i == 0:
            return False
    return True


def encrypt(plain: str, key: int) -> str:
    cipher = ''
    counter = 0
    for ch in plain:
        code = (key*get_code(ch) + 4) % NUM_VALID
        cipher += get_char(code)
        counter += 1
        if counter % 20 == 0:
            key += 1
            while not is_prime(key):
                key += 1
    return cipher


def decrypt(cipher: str, key: int) -> str:
    plain = ''
    counter = 0
    for ch in cipher:
        code = (modulo_mul_inverse(key, NUM_VALID)
                * (get_code(ch) - 4)) % NUM_VALID
        plain += get_char(code)
        counter += 1
        if counter % 20 == 0:
            key += 1
            while not is_prime(key):
                key += 1
    return plain


def main():
    stream = open("plain.txt")
    output = open("cipher.txt", "w")
    print("CIPHER")
    cipher = encrypt(stream.read(), KEY)
    print(cipher)
    stream.close()
    output.write(cipher)
    output.close()
    print("DECIPHER")
    plain = decrypt(cipher, KEY)
    print(plain)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

'''
[OUTPUT]

CIPHER
$'uf'^BGv'$$FG'vPg5G 0E\5'j`\   Cxj5cz  >`aRo!y[CHHefNfjy0}H&f]Yq2_Ue_|`pNUqT=`\qU
DECIPHER
sarka: classical-encryption-techniques-duskygloom % python .\playfair_cypher.py
'''
