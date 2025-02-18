from cipher_utils import *

DIGRAM_SIZE = 10
KEY = "A quick brown fox LEAPS OVER a BLUE Well"

class Digram:
    __size: int
    __matrix: list[list[str]]
    __filler1: str = ' '
    __filler2: str = '.'

    def __init__(self, size: int, key: str):
        self.__size = size
        self.__matrix = [['' for j in range(size)] for i in range(size)]
        row = col = 0
        for i in key + ''.join(VALID_CH):
            if i in self:
                continue
            self.__matrix[row%size][col%size] = i
            col += 1
            if col % size == 0:
                row += 1
        # fill unfilled cells
        counter = 0
        for i in range(size-1, -1, -1):
            for j in range(size-1, -1, -1):
                if self.__matrix[i][j] == '':
                    self.__matrix[i][j] = chr(256+counter)
                    counter += 1

    def index(self, ch: str) -> tuple[int, int]:
        '''
        Returns
        -------
        Returns (x, y) where ch is located in digram.
        Returns (-1, -1) if ch is not present in digram.
        '''
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__matrix[i][j] == ch:
                    return (i, j)
        return (-1, -1)
    
    def __encrypt_sub(self, duo: str) -> str:
        if len(duo) != 2:
            return ""
        index1 = self.index(duo[0])
        index2 = self.index(duo[1])
        if index1 == -1 or index2 == -1:
            return ""
        if index1[0] == index2[0]:                                              # same row
            return self[index1[0], (index1[1]+1)%self.__size] \
                + self[index2[0], (index2[1]+1)%self.__size]
        elif index1[1] == index2[1]:                                            # same col
            return self[(index1[0]+1)%self.__size, index1[1]] \
                + self[(index2[0]+1)%self.__size, index2[1]]
        else:                                                                   # rectangular
            return self[index1[0], index2[1]] \
                + self[index2[0], index1[1]]
    
    def __decrypt_sub(self, duo: str) -> str:
        if len(duo) != 2:
            return ""
        index1 = self.index(duo[0])
        index2 = self.index(duo[1])
        if index1 == -1 or index2 == -1:
            return ""
        if index1[0] == index2[0]:                                              # same row
            return self[index1[0], (index1[1]-1)%self.__size] \
                + self[index2[0], (index2[1]-1)%self.__size]
        elif index1[1] == index2[1]:                                            # same col
            return self[(index1[0]-1)%self.__size, index1[1]] \
                + self[(index2[0]-1)%self.__size, index2[1]]
        else:                                                                   # rectangular
            return self[index1[0], index2[1]] \
                + self[index2[0], index1[1]]
    
    def encrypt(self, plain: str) -> str:
        cipher = ''
        length = len(plain)
        i = 0
        while i < length:
            if i == length-1 or plain[i] == plain[i+1]:                             # have to add filler
                if plain[i] == Digram.__filler1:
                    cipher += self.__encrypt_sub(plain[i] + Digram.__filler2)
                else:                                                               # filler2 is used if filler1 is next
                    cipher += self.__encrypt_sub(plain[i] + Digram.__filler1)
                i += 1
            else:                                                                   # dont have to add filler
                cipher += self.__encrypt_sub(plain[i] + plain[i+1])
                i += 2
        return cipher
    
    def decrypt(self, cipher: str) -> str:
        plain = ''
        length = len(cipher)
        i = 0
        while i < length:
            if i == length-1 or cipher[i] == cipher[i+1]:                           # have to add filler
                if cipher[i] == Digram.__filler1:
                    plain += self.__decrypt_sub(cipher[i] + Digram.__filler2)
                else:                                                               # filler2 is used if filler1 is next
                    plain += self.__decrypt_sub(cipher[i] + Digram.__filler1)
                i += 1
            else:                                                                   # dont have to add filler
                plain += self.__decrypt_sub(cipher[i] + cipher[i+1])
                i += 2
        return plain

    def __str__(self) -> str:
        if len(self.__matrix) == 0:
            return ''
        s = self.__matrix[0].__str__()
        for i in range(1, self.__size):
            s += '\n' + self.__matrix[i].__str__()
        return s
    
    def __contains__(self, ch: str) -> bool:
        for i in self.__matrix:
            if ch in i:
                return True
        return False
    
    def __getitem__(self, index: tuple[int, int]) -> str:
        '''
        Returns
        -------
        Returns char at index, index is a tuple containing x and y.
        If x and y not in digram, returns null character.
        '''
        if not (isinstance(index, tuple) and len(index) == 2):
            return '\0'
        if index[0] < self.__size and index[1] < self.__size:
            return self.__matrix[index[0]][index[1]]
        return '\0'

def main():
    stream = open("plain.txt", encoding='utf-8')
    output = open("cipher.txt", "w", encoding='utf-8')
    d = Digram(DIGRAM_SIZE, KEY)
    cipher = d.encrypt(stream.read())
    stream.close()
    output.write(cipher)
    output.close()
    print("CIPHER")
    print(cipher)
    plain = d.decrypt(cipher)
    print("DECIPHER")
    print(plain)

if __name__ == "__main__":
    main()

'''
[OUTPUT]

CIPHER
`
obW7qk  B`rhr ea2aEkoĂ`ho V5`'E`LcucU`4gqmr{`!kktu#b`Ā`tian3Tm  # nBcojAĂ`jWq4`Ă
DECIPHER
sarka: clas sical-encryption-techniques-duskygloom % python .\playfair_cypher.py
'''
