import random
import numpy as np
from cipher_utils import *

SEED = 10
KEY_SIZE = 8
KEY_LOWER = 11
KEY_UPPER = 197

class Key:
    __mat: list[list[int]]
    __filler: str = ' '

    def __init__(self, matrix: list[list[int]]):
        rows = len(matrix)
        for row in matrix:
            if len(row) != rows:
                raise ValueError("Square matrix expected.")
        self.__mat = matrix

    @property
    def size(self) -> int:
        return len(self.__mat)
    
    @staticmethod
    def random2dlist(size: int) -> list[list[int]]:
        return [[random.randint(KEY_LOWER, KEY_UPPER) for i in range(size)] for j in range(size)]
    
    def encrypt(self, plain: str) -> str:
        s = [-1 for i in range(self.size)]
        cipher = ''
        counter = 0
        while counter < len(plain):
            for i in range(self.size):
                s[i] = get_code(plain[counter] if counter < len(plain) else self.__filler)
                counter += 1
            for i in range(self.size):
                code = 0
                for j in range(self.size):
                    code += s[j] * self[j, i]
                cipher += get_char(code % NUM_VALID)
        return cipher
    
    @staticmethod
    def determinant(mat: list[list[int]]) -> int:
        if len(mat) == 1:
            return mat[0][0]
        det = 0
        for i in range(len(mat)):                                                                   # considering square matrix
            det += (1 if i%2 == 0 else -1) * mat[0][i] * Key.determinant(Key.minor(mat, 0, i))
        return det
    
    @staticmethod
    def minor(mat: list[list[int]], x: int, y: int) -> list[list[int]]:
        '''
        Parameters
        ----------
        mat : matrix on which operation is done
        x : row to be removed
        y : column to be removed
        '''
        size = len(mat)
        minor = [[0 for i in range(size-1)] for j in range(size-1)]
        row = 0; col = 0
        for i in range(size):
            if i == x:
                continue
            col = 0
            for j in range(size):
                if j != y:
                    minor[row][col] = mat[i][j]
                    col += 1
            row += 1
        return minor
    
    @staticmethod
    def adjacent(mat: list[list[int]]) -> list[list[int]]:
        size = len(mat)
        adj = [[0 for i in range(size)] for j in range(size)]
        for i in range(size):
            for j in range(size):
                sign = -2 * ((i+j) % 2) + 1
                adj[j][i] = (1 if (i+j)%2 == 0 else -1) * Key.determinant(Key.minor(mat, i, j))
        return adj
    
    def __mod_adjacent(self) -> list[list[int]]:
        return [[j % NUM_VALID for j in i] for i in Key.adjacent(self.__mat)]
    
    def __mod_det_inverse(self) -> int:
        det = Key.determinant(self.__mat) % NUM_VALID
        return modulo_mul_inverse(det, NUM_VALID)
        
    def __mod_inverse(self) -> list[list[int]]:
        adj = self.__mod_adjacent()
        det_inverse = self.__mod_det_inverse()
        return [[(det_inverse * i) % NUM_VALID for i in j] for j in adj]
    
    def decrypt(self, cipher: str) -> str:
        s = [-1 for i in range(self.size)]
        plain = ''
        key = self.__mod_inverse()
        counter = 0
        while counter < len(cipher):
            for i in range(self.size):
                s[i] = get_code(cipher[counter] if counter < len(cipher) else self.__filler)
                counter += 1
            for i in range(self.size):
                code = 0
                for j in range(self.size):
                    code += s[j] * key[j][i]
                plain += get_char(code % NUM_VALID)
        return plain

    def __str__(self):
        if len(self.__mat) == 0:
            return ''
        s = self.__mat[0].__str__()
        for i in range(1, self.size):
            s += '\n' + self.__mat[i].__str__()
        return s
    
    def __getitem__(self, index: tuple[int, int]) -> str:
        '''
        Returns
        -------
        Returns char at index, index is a tuple containing x and y.
        If x and y not in digram, returns null character.
        '''
        if not (isinstance(index, tuple) and len(index) == 2):
            raise ValueError("Invalid index.")
        if index[0] < self.size and index[1] < self.size:
            return self.__mat[index[0]][index[1]]
        raise ValueError("Index out of bounds.")

def main():
    stream = open("plain.txt")
    output = open("cipher.txt", "w")
    k = Key(Key.random2dlist(KEY_SIZE))
    cipher = k.encrypt(stream.read())
    stream.close()
    output.write(cipher)
    output.close()
    print("CIPHER")
    print(cipher)
    plain = k.decrypt(cipher)
    print("DECIPHER")
    print(plain)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

'''
[OUTPUT]

CIPHER
v<;TejxaP=9xWk:=2yig'Sj AG^SwWME:!?k^3v:"i1"`8dmG*wM-d.G9JIW.ilvdq59, M#&^]KWIH)
DECIPHER
sarka: classical-encryption-techniques-duskygloom % python .\playfair_cypher.py
'''
