from cipher_utils import *

KEY = "A quick brown fox LEAPS OVER a BLUE Well"

class Tableau:
    __table: list[list[int]]

    def __init__(self, size: int):
        self.__table = [[(i+j)%size for i in range(size)] for j in range(size)]

    def __len__(self)  -> int:
        return len(self.__table)
    
    def __getitem__(self, index: tuple[int, int]) -> int:
        if isinstance(index, tuple):
            if len(index) != 2:
                raise ValueError("Expected two arguments.")
            return self.__table[index[0]][index[1]]
    
    def __str__(self):
        if len(self.__table) == 0:
            return ''
        s = self.__table[0].__str__()
        for i in range(1, len(self)):
            s += '\n' + self.__table[i].__str__()
        return s
    
    def encrypt(self, plain: str, key: str) -> str:
        cipher = ''
        counter = 0
        while counter < len(plain):
            code = self[get_code(plain[counter]), get_code(key[counter%len(key)])]
            cipher += get_char(code)
            counter += 1
        return cipher
    
    def index_in_row(self, ch: str, row: int) -> int:
        '''
        Returns
        -------
        Returns the index of ch in row.
        '''
        return self.__table[row].index(get_code(ch))
    
    def decrypt(self, ciph: str, key: str) -> str:
        plain = ''
        counter = 0
        while counter < len(ciph):
            code = self.index_in_row(ciph[counter], get_code(key[counter%len(key)]))
            plain += get_char(code)
            counter += 1
        return plain

def main():
    stream = open("plain.txt")
    output = open("cipher.txt", "w")
    t = Tableau(NUM_VALID)
    ciph = t.encrypt(stream.read(), KEY)
    stream.close()
    output.write(ciph)
    output.close()
    print("CIPHER")
    print(ciph)
    plain = t.decrypt(ciph, KEY)
    print("DECIPHER")
    print(plain)

if __name__ == "__main__":
    main()

'''
[OUTPUT]

CIPHER
5cdaK   meOTckXeH\&g;)4JDv9F4avGe+;?7w=Y{Q7u]oQP[qPtvy_{[XhpNU  A@cI='<tAe<=>+tgVf
DECIPHER
sarka: classical-encryption-techniques-duskygloom % python .\playfair_cypher.py
'''
