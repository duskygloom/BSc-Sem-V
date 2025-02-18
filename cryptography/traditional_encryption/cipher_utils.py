import math

VALID_CH: list[str] = ['\t', '\n'] + [chr(i) for i in range(32, 127)]
NUM_VALID = len(VALID_CH)

def is_valid_char(ch: str) -> bool:
    return ch in VALID_CH

def get_code(ch: str) -> int:
    '''
    Returns
    -------
    Code equivalent of the char.
    Returns -1 if ch in not a valid char.
    '''
    if ch in VALID_CH:
        return VALID_CH.index(ch)
    return -1

def get_char(code: int) -> str:
    '''
    Returns
    -------
    Char equivalent of the code.
    Returns null char if not a valid code.
    '''
    if code < 0 or code >= len(VALID_CH):
        return '\0'
    return VALID_CH[code]

def modulo_mul_inverse(x: int, m: int) -> int:
    '''
    Returns
    -------
    Returns (1/x) mod m.
    '''
    if x == 0:
        raise ArithmeticError("Inverse is not defined if determinant is zero.")
    if math.gcd(x, m) != 1:
        raise ArithmeticError("Modular inverse for this key is not defined.")
    inv = 1
    while inv < m and (x * inv) % m != 1:
        inv += 1
    return inv

def modulo_mul_inverse_euclid(x: int, m: int) -> int:
    r1, r2 = m, x
    t1, t2 = 0, 1
    while r2 != 0:
        q = r1 // r2
        r1, r2 = r2, r1 - r2*q
        t1, t2 = t2, t1 - t2*q
    if r1 == 1:
        return t1 % m
    raise ArithmeticError("Modular inverse for this key is not defined.")
