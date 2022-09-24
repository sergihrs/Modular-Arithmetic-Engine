from rword import random_word
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
    for i in range(3, math.floor(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def lista_primos(a: int, b: int) -> list[int]:
    """
    Z x Z -> [Z]
    Devuelve una lista de los numeros primos en [a, b)
    """
    return a, b


def factorizar(n: int) -> dict[int, int]:
    """
    Z -> {Z: Z}
    Devuelve un diccionario con los factores primos de n y sus exponentes
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


def mcd(a: int, b: int) -> int:
    """
    Z x Z -> Z
    Devuelve el maximo comun divisor de a y b
    """
    return a, b


def bezout(a: int, b: int) -> tuple[int, int, int]:
    """
    Z x Z -> (Z, Z, Z)
    Devuelve una tupla (d,x,y) donde d es el (a,b) y (x,y) es una solucion particular de d = ax + by
    """
    return a, b


def mcd_n(nlist: list[int] | int) -> int:
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
    return a, b


def potencia_mod_p(base: int, exp: int, p: int) -> int:
    """
    Z x Z x Z -> Z
    Devuelve base^exp mod p
    """
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
    """
    return n, p


def euler(n: int) -> int:
    """
    Z -> Z
    Devuelve el valor de euler phi de n
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
    Z x Z -> Z
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


def simplificar_expresion(expresion: str) -> str:
    """
    str -> str
    Simplifica una expresion algebraica
    """
    return random_word()


def tabla_verdad_a_expresion(tabla_verdad: list[int]) -> str:
    """
    [Bool] -> str
    Devuelve una expresion algebraica que representa la tabla de verdad
    """
    return random_word()


if __name__ == "__main__":
    print("es_primo:")
    print(timeit.timeit("print(es_primo(1000000007))", globals=globals(), number=1))
    print("lista_primos:")
    print(timeit.timeit("print(lista_primos(1, 1000000))", globals=globals(), number=1))
    print("factorizar:")
    print(
        timeit.timeit(
            "factorizar(n)",
            setup="n=2**4 * 3**4 * 7**2 * 11 * 13**2 * 97**2",
            globals=globals(),
            number=1000000,
        )
    )
    print("potencia_mod_p:")
    print(
        timeit.timeit(
            "potencia_mod_p(12,13241324323312345678765,17)",
            globals=globals(),
            number=1,
        )
    )
