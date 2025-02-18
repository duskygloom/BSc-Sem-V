import os
import sys
import random
from cipher_utils import *

SEED = 10
KEYS = (11, 7, 13, 3, 11, 17, 3, 19, 5)

def encrypt(plain: str, keys: list[int], seed: int):
    cipher = ''
    counter = 0
    random.seed(seed)
    for ch in plain:
        if not is_valid_char(ch):
            continue
        else:
            cipher += get_char((get_code(ch) + keys[counter % len(keys)]) % NUM_VALID)
        counter += 1
        if counter % 10 == 0:
            random.shuffle(keys)
    return cipher

def decrypt(ciph: str, keys: list[int], seed: int):
    plain = ''
    counter = 0
    random.seed(seed)
    for ch in ciph:
        if not is_valid_char(ch):
            continue
        else:
            plain += get_char((get_code(ch) - keys[counter % len(keys)]) % NUM_VALID)
        counter += 1
        if counter % 10 == 0:
            random.shuffle(keys)
    return plain

def main():
    stream = open("plain.txt")
    output = open("cipher.txt", "w")
    print("CIPHER")
    cipher = encrypt(stream.read(), list(KEYS), SEED)
    stream.close()
    output.write(cipher)
    output.close()
    print(cipher)
    print("DECIPHER")
    plain = decrypt(cipher, list(KEYS), SEED)
    print(plain)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

'''
[OUTPUT]

CIPHER
~h      nlK#vql
%phlo0p pu|w    z!s:    hfoyl~
x#2gz#n#noz!z%,%{%      {
q#5gsol~sh|"jf#ukl      A #
DECIPHER
sarka: classical-encryption-techniques-duskygloom % python .\playfair_cypher.py
'''
