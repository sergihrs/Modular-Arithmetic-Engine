import math
import numpy as np
import random


def a_sprp(n: int, a: int) -> bool:
    """
    Z x Z -> Bool
    Comprueba si n es un primo probable con fermat
    """
    d = n - 1
    s = 0
    while d % 2 == 0:
        d = d >> 1
        s += 1
    x = potencia_mod_p(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s):
        x = (x * x) % n
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False


def es_primo(n: int) -> bool:
    """
    Z -> Bool
    Comprueba si n es un primo con miller
    """
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    if n <= 2047:
        bases = [2]
    elif n <= 1373653:
        bases = [2, 3]
    elif n <= 25326001:
        bases = [2, 3, 5]
    elif n <= 3215031751:
        bases = [2, 3, 5, 7]
    if n == 3215031751:
        return False
    for a in bases:
        if not a_sprp(n, a):
            return False
    return True


def lista_primos(a: int, b: int) -> list[int]:
    """
    Z x Z -> [Z]
    Devuelve una lista de los numeros primos en [a, b)
    """
    root = int(math.sqrt(b))
    primos = []
    es_primo = [True] * root
    for i in range(2, root):
        if es_primo[i]:
            primos.append(i)
            for j in range(i * i, root, i):
                es_primo[j] = False
    es_primo_ab = [True] * (b - a)
    for primo in primos:
        for i in range(primo + ((-a) % primo), b - a, primo):
            es_primo_ab[i] = False
    primos_ab = []
    for i in range(b - a):
        if es_primo_ab[i]:
            primos_ab.append(i + a)
    return primos_ab


def factorizar_simple(n: int):
    """
    Returns the prime factors of n in a dictionary in O(sqrt(n))
    """
    factors = dict()
    while n % 2 == 0:
        n = n >> 2
        factors[2] = factors.get(2, 0) + 1
    for i in range(3, math.floor(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            n //= i
            factors[i] = factors.get(i, 0) + 1
        if n == 1:
            return factors
    if n != 1:
        factors[n] = 1
    return factors


def factorizar(n: int) -> dict[int, int]:
    """
    Z -> {Z: Z, ...}
    Devuelve un diccionario con los factores primos de n y sus exponentes
    If n is 0 or 1, raise an exception ?
    """

    factors = dict()
    firsts = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for primo in firsts:
        c = 0
        while n % primo == 0:
            n //= primo
            c += 1
        if c != 0:
            factors[primo] = c
    if n < 10**10:
        return {**factors, **factorizar_simple(n)}
    else:
        g = lambda x: (x**2 + 1) % n
        x = 1
        while x < 5:
            x += 1
            y = x
            d = 1
            while d == 1:
                x = g(x)
                y = g(g(y))
                d = mcd(abs(x - y), n)
            if d != n:
                return {**factors, **factorizar(d), **factorizar(n // d)}
        return {**factors, **factorizar_simple(n)}


def mcd(*args: int) -> int:
    """
    Z x Z x Z x ... -> Z
    Devuelve el máximo común divisor de todos los números
    1->1? 0->inf?
    negative numbers?
    """
    a, b = min(args), max(args)
    while a:
        a, b = b % a, a
    return b


def bezout(a: int, b: int) -> tuple[int, int, int]:
    """
    Z x Z -> (Z, Z, Z)
    Devuelve una tupla (d,x,y) donde d es el mcd(a,b) y (x,y) es una solucion particular de d = ax + by
    """
    a_coeffs = np.array([1, 0])
    b_coeffs = np.array([0, 1])

    while a:
        a_coeffs, b_coeffs = b_coeffs - a_coeffs * (b // a), a_coeffs
        a, b = b % a, a

    return b, *b_coeffs


def mcd_n(nlist: list[int]) -> int:
    """
    [Z] -> Z
    Devuelve el maximo comun divisor de los numeros de nlist
    """
    return nlist


def bezout_n(nlist: list[int]) -> tuple[int, list[int]]:
    """
    [Z] -> (Z, [Z])
    Devuelve una tupla (d,x) donde d es el mcd de los coeficientes y x es una solucion particular
    de d = c1*x1 + c2*x2 + ... + cn*xn
    """
    return nlist


def coprimos(a: int, b: int) -> bool:
    """
    Z x Z -> Bool
    Comprueba si dos numeros son coprimos
    """
    if (a | b) & 1 == 0:
        return False
    return mcd(a, b) == 1


def potencia_mod_p(base: int, exp: int, p: int) -> int:
    """
    Z x Z x Z -> Z
    Devuelve base^exp mod p
    Raise an exception if exp < 0 and base is not invertible mod p
    """

    base %= p

    if exp < 0:
        base = inverso_mod_p(base, p)
        exp = -exp
    elif exp == 0:
        return 1
    elif exp == 1:
        return base
    potencia = 1
    bin_str = bin(exp)
    for i in range(len(bin_str) - 1, 1, -1):
        if bin_str[i] == "1":
            potencia = (potencia * base) % p
        base = (base * base) % p
    return potencia


def inverso_mod_p(n: int, p: int) -> int:
    """
    Z x Z -> Z
    Devuelve el inverso de n mod p
    Raise an exception if n is not invertible mod p
    """

    n = n % p

    if p == 1 or not coprimos(n, p):
        raise ValueError(f"{n} no tiene inversa mod {p} (NE)")

    a_comb = 1
    b_comb = 0

    while n:
        a_comb, b_comb = b_comb - a_comb * (p // n), a_comb
        p, n = n, p % n

    return b_comb


def euler(n: int) -> int:
    """
    Z -> Z
    Devuelve el valor de euler totient of n
    If n is negative, raise an exception ?
    """
    primos = factorizar(n).keys()
    tot = n
    for primo in primos:
        tot -= tot / primo
    return tot


def legendre(n: int, p: int) -> int:
    """
    Z x Z -> Z
    Devuelve el simbolo de legendre de n y p
    """
    return potencia_mod_p(n, (p - 1) // 2, p)


def resolver_sistema_congruencias(
    alist: list[int], blist: list[int], plist: list[int]
) -> tuple[int, list[int]]:
    """
    [Z] x [Z] x [Z] -> (Z, [Z])
    Resuelve el sistema de congruencias lineal y devuelve una tupla (r,m) donde r es la solucion modulo m
    """
    size = len(plist)
    for k in range(size):
        a = alist[k]
        b = blist[k]
        p = plist[k]
        gcd = mcd(mcd(a, b), p)
        if gcd > 1:
            alist[k] = a//gcd
            blist[k] = b//gcd
            plist[k] = p//gcd

    # for k1, p1 in enumerate(plist):
    #     for p2 in plist[k1+1:]:
    #         gcd = mcd(p1, p2)
    #         if gcd > 1:
    #             raise ValueError(f"Los números {p1} y {p2} no son coprimos, tienen mcd={gcd}")

    m = 1
    for p in plist:
        m *= p

    x = 0
    for a, b, p in zip(alist, blist, plist):
        nk = m//p
        xk = inverso_mod_p(nk, p)
        a_inv = inverso_mod_p(a, p)
        x += nk*xk*a_inv

    return x%m, m


def raiz_mod_p(n: int, p: int) -> int:
    """
    Z x Z -> Z (Tupla ?)
    Devuelve una raiz cuadrada de n mod p
    - Si n tiene dos raices distintas x1 < x2, las escribe en orden: “x1, x2”
    - Si n tiene una unica raiz x, escribe “x”
    - Si n no tiene raices, como con el resto de comandos, escribe “NE” en modo “batch” o un mensaje de error
    adecuado en modo interactivo.
    """
    return n, p


def ecuacion_cuadratica(a: int, b: int, c: int, p: int) -> tuple[int, int]:
    """
    Z x Z x Z x Z -> (Z, Z)
    Devuelve una solucion de la ecuacion ax^2 + bx + c = 0 mod p
    - Si la ecuacion tiene dos raices distintas x1 < x2, las escribe en orden: “x1, x2”
    - Si la ecuacion tiene una unica raiz doble x, escribe “x”
    - Si la ecuacion no tiene raices, como con el resto de comandos, escribe “NE” en modo “batch” o un mensaje de
    error adecuado en modo interactivo.
    """
    discrim = raiz_mod_p(b**2-4*a*c, p)
    den_inv = inverso_mod_p(2*a, p)
    sol1 = ((-b+discrim)*den_inv)%p
    sol2 = ((-b-discrim)*den_inv)%p
    return sol1, sol2


# def simplificar_expresion(expresion: str) -> str:
#     """
#     str -> str
#     Simplifica una expresion algebraica
#     """
#     return random_word()


# def tabla_verdad_a_expresion(tabla_verdad: list[int]) -> str:
#     """
#     [Bool] -> str
#     Devuelve una expresion algebraica que representa la tabla de verdad
#     """
#     return random_word()


if __name__ == "__main__":
    # print("es_primo:")
    # print(timeit.timeit("print(es_primo(1000000007))", globals=globals(), number=1))
    # print("lista_primos:")
    # print(timeit.timeit("lista_primos(1, 1000000)", globals=globals(), number=1))
    # print("factorizar:")
    # print(
    #     timeit.timeit(
    #         "print(factorizar(n))",
    #         setup="n=280951972823",
    #         globals=globals(),
    #         number=1,
    #     )
    # )
    # print("mcd:")
    # print(
    #     timeit.timeit(
    #         "print(mcd(1200901,1939917))",
    #         globals=globals(),
    #         number=1,
    #     )
    # )
    # print("bezout:")
    # print(
    #     timeit.timeit(
    #         "print(bezout(99, 105))",
    #         globals=globals(),
    #         number=1,
    #     )
    # )
    # print("potencia_mod_p:")
    # print(
    #     timeit.timeit(
    #         "potencia_mod_p(12,13241324323312345678765,17)",
    #         globals=globals(),
    #         number=1,
    #     )
    # )
    # print("inversa_mod_p:")
    # print(
    #     timeit.timeit(
    #         "print(inverso_mod_p(212207101440105399533740733471,343358302784187294870275058337))",
    #         globals=globals(),
    #         number=10,
    #     )
    #     / 10
    # )
    pass
    # for i in range(2, 100):
    #     if miller_test(i):
    #         print(i)
    # print(miller_test(4))
    # print(sprp(4, 2))
    print(resolver_sistema_congruencias([6519037604], [8972153143], [1297334945]))
