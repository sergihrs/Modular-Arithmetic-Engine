import math
import timeit


def es_primo(n: int) -> bool:
    """
    Z -> Bool
    Comprueba si un numero entero es primo
    """
    if n < 2:
        return False
    if n % 2 == 0:
        return False
    if 2 ** (n - 1) % n != 1:
        return False
    for i in range(3, math.floor(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def lista_primos(a: int, b: int) -> list[int]:
    """
    Z x Z -> [Z]
    Devuelve una lista de los numeros primos en [a, b)
    """
    root = math.floor(math.sqrt(b))
    primos_potenciales = [True]*root
    primos = []
    primos_en_rango = [True]*(b-a)
    sol = []

    for primo in range(2, root):
        if primos_potenciales[primo]:
            primos.append(primo)
            for num in range(primo**2, root, primo):
                primos_potenciales[num] = False
    
    for primo in primos:
        for num in range((-a)%primo, b-a, primo):
            primos_en_rango[num] = False
    
    for i, primo in enumerate(primos_en_rango):
        if primo:
            sol.append(i+a)

    return sol


def factorizar(n: int) -> dict[int, int]:
    """
    Z -> {Z: Z, ...}
    Devuelve un diccionario con los factores primos de n y sus exponentes
    If n is 0 or 1, raise an exception ?
    """
    f = {}
    i = 2
    while n > 1:
        e = 0
        while n % i == 0:
            n //= i
            e += 1
        if e > 0:
            f[i] = e
        i += 1
    return f


def mcd(*args: int) -> int:
    """
    Z x Z x Z x ... -> Z
    Devuelve el maximo comun divisor de todos los numeros
    """
    if len(args) == 2:
        a, b = args
        a, b = min(a, b), max(a, b)
        while a != 0:
            a, b = b, b % a
            a, b = min(a, b), max(a, b)
        return b


def bezout(a: int, b: int) -> tuple[int, int, int]:
    """
    Z x Z -> (Z, Z, Z)
    Devuelve una tupla (d,x,y) donde d es el gcd(a,b) y (x,y) es una solucion particular de d = ax + by
    """
    return a, b


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
    return mcd(a, b) == 1


def potencia_mod_p(base: int, exp: int, p: int) -> int:
    """
    Z x Z x Z -> Z
    Devuelve base^exp mod p
    Raise an exception if exp < 0 and base is not invertible mod p
    """
    if exp < 0 and mcd(base, p) != 1:
        raise ValueError("Base must be invertible mod p")
    if exp == 0:
        return 1
    if exp == 1:
        return base % p
    potencia = 1
    for bit in bin(exp)[:1:-1]:
        if bit == "1":
            potencia = (potencia * base) % p
        base = (base * base) % p
    return potencia


def inverso_mod_p(n: int, p: int) -> int:
    """
    Z x Z -> Z
    Devuelve el inverso de n mod p
    Raise an exception if n is not invertible mod p
    """
    return n, p


def euler(n: int) -> int:
    """
    Z -> Z
    Devuelve el valor de euler phi de n
    If n is negative, raise an exception ?
    """
    return n


def legendre(n: int, p: int) -> int:
    """
    Z x Z -> Z
    Devuelve el simbolo de legendre de n y p
    """
    return n, p


def resolver_sistema_congruencias(
    alist: list[int], blist: list[int], plist: list[int]
) -> tuple[int, list[int]]:
    """
    [Z] x [Z] x [Z] -> (Z, [Z])
    Resuelve el sistema de congruencias lineal y devuelve una tupla (r,m) donde r es la solucion modulo m
    """
    return alist, blist, plist


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
    return a, b, c, p


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
    print("lista_primos:")
    print(timeit.timeit("lista_primos(90000000, 100000000)", globals=globals(), number=1))
    # print("factorizar:")
    # print(
    #     timeit.timeit(
    #         "factorizar(n)",
    #         setup="n=2**4 * 3**4 * 7**2 * 11 * 13**2 * 97**2",
    #         globals=globals(),
    #         number=1000000,
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
