from cipher_utils import *

import random

SEED = 10
N_STAGES = 3
KEY_LOWER = 30
KEY_UPPER = 127                                             # exclusive
KEY_RANGE = KEY_UPPER - KEY_LOWER


class Rotor:
    __stages: list[list[int]]
    __offset: list[int]

    def __init__(self, seed: int):
        '''
        Parameters
        ----------
        seed : seed for random number generator
        '''
        random.seed(seed)
        self.__stages = [list(range(KEY_LOWER, KEY_UPPER))
                         for i in range(N_STAGES)]
        for i in self.__stages:
            random.shuffle(i)
        self.__offset = [0 for i in range(N_STAGES)]

    def reset(self):
        for i in range(N_STAGES):
            self.__offset[i] = 0

    def rotate(self, value: int = 1):
        self.__offset[0] += value
        for i in range(N_STAGES-1):
            self.__offset[i+1] = self.__offset[i] // KEY_RANGE

    def index(self, value: int, stage: int) -> int:
        if value < KEY_LOWER or value >= KEY_UPPER:
            raise ValueError(f"Invalid value: should be within [{
                             KEY_LOWER}, {KEY_UPPER})")
        if stage < 0 or stage >= N_STAGES:
            raise ValueError(
                f"Invalid stage: should be within [0, {N_STAGES})")
        return (self.__stages[stage].index(value) - self.offset[stage]) % KEY_RANGE

    def encrypt(self, plain: str) -> str:
        cipher = ''
        for i in plain:
            if not is_valid_char(i):
                continue
            '''
            PROCEDURE
            ---------
            code
                code = [index] - 30
                ... for all stages ...
            rotate
            '''
            code = get_code(i)
            for j in range(N_STAGES):
                # print(f"({code}, {get_char(code)}) -> [{code}] = {self[j, code]} -> ({self[j, code]-KEY_LOWER}, {get_char(self[j, code]-KEY_LOWER)})")
                code = self[j, code] - KEY_LOWER
            # print()
            cipher += get_char(code)
            self.rotate()
        return cipher

    def decrypt(self, ciph: str) -> str:
        plain = ''
        for i in ciph:
            if not is_valid_char(i):
                continue
            '''
            PROCEDURE
            ---------
            code
                code = index(code + 30)
                ... for all stages ...
            rotate
            '''
            code = get_code(i)
            for j in range(N_STAGES-1, -1, -1):
                # print(f"({code}, {get_char(code)}) -> index({code+KEY_LOWER}) = {self.index(code + KEY_LOWER, j)} -> ({self.index(code + KEY_LOWER, j)}, {get_char(self.index(code + KEY_LOWER, j))})")
                code = self.index(code + KEY_LOWER, j)
            # print()
            plain += get_char(code)
            self.rotate()
        return plain

    def __getitem__(self, index: tuple[int]) -> int:
        if not (isinstance(index, tuple) and len(index) == 2):
            raise SyntaxError("Expected stage and index as a tuple.")
        if index[0] < 0 or index[0] >= N_STAGES:
            raise ValueError(
                f"Invalid stage: should be within [0, {N_STAGES})")
        if index[1] < 0 or index[1] >= KEY_RANGE:
            raise ValueError(
                f"Invalid index: should be within [0, {KEY_RANGE})")
        return self.__stages[index[0]][(index[1]+self.offset[index[0]]) % KEY_RANGE]

    def __str__(self):
        if N_STAGES < 1:
            return ''
        stages = self.__stages
        s = (stages[0][self.offset[0] % KEY_RANGE:]+stages[0]
             [:self.offset[0] % KEY_RANGE]).__str__()
        for i in range(1, N_STAGES):
            s += '\n' + (stages[i][self.offset[i] % KEY_RANGE:] +
                         stages[i][:self.offset[i] % KEY_RANGE]).__str__()
        return s

    @property
    def offset(self) -> tuple[int]:
        return tuple(self.__offset)


def main():
    stream = open("plain.txt")
    output = open("cipher.txt", "w")
    rotor = Rotor(SEED)
    cipher = rotor.encrypt(stream.read())
    stream.close()
    output.write(cipher)
    output.close()
    print("CIPHER")
    print(cipher)
    print("DECIPHER")
    rotor.reset()
    print(rotor.decrypt(cipher))


if __name__ == "__main__":
    main()

'''
[OUTPUT]
CIPHER
03wYJ$b2w2+~
RoXNi/i.e.V?99jnp?be:Ik(k5VKE!#I,KNK;O5#-*accyPkd*$     cDux#j{O @]Z]r
DECIPHER
sarka: classical-encryption-techniques-duskygloom % python .\playfair_cypher.py
'''
