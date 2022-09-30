import math
import timeit
import numpy as np
import random


class Module:
    def __init__(self):
        self.cache = {}

    def a_sprp_module(self, n: int, a: int) -> bool:
        """
        Z x Z -> Bool
        Comprueba si n es un primo probable con fermat
        """
        d = n - 1
        s = 0
        while d % 2 == 0:
            d = d >> 1
            s += 1
        x = self.potencia_mod_p_module(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s):
            x = (x * x) % n
            if x == 1:
                return False
            if x == n - 1:
                return True
        return False

    def es_primo_module(self, n: int) -> bool:
        """
        Z -> Bool
        Comprueba si n es un primo con miller
        """
        if n <= 1 or n == 4:
            return False
        if n <= 3:
            return True
        exceptions = [25326001, 161304001, 960946321]
        if n in exceptions:
            return False
        if n <= 2047:
            bases = [2]
        elif n <= 1373653:
            bases = [2, 3]
        else:
            bases = [2, 3, 5]
        for a in bases:
            if not self.a_sprp_module(n, a):
                return False
        return True

    def lista_primos_module(self, a: int, b: int) -> list[int]:
        """
        Z x Z -> [Z]
        Devuelve una lista de los numeros primos en [a, b)
        """
        a = max(a, 2)
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

    def factorizar_simple_module(self, n: int):
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

    def factorizar_module(self, n: int) -> dict[int, int]:
        """
        Z -> {Z: Z, ...}
        Devuelve un diccionario con los factores primos de n y sus exponentes
        If n is 0 or 1, raise an exception ?
        """
        if n == 1:
            return {1: 1}
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
            return {**factors, **self.factorizar_simple_module(n)}
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
                    return {
                        **factors,
                        **self.factorizar_module(d),
                        **self.factorizar_module(n // d),
                    }
            return {**factors, **self.factorizar_simple_module(n)}

    def mcd_module(self, *args: int) -> int:
        """
        Z x Z -> Z
        Devuelve el maximo comun divisor de a y b usando least absolute remainder. Mio
        """
        a, b = args
        if a < b:
            while a:
                r, b = b % a, a
                if r > a >> 1:
                    a = a - r
                else:
                    a = r
            return b
        else:
            while b:
                r, b = a % b, b
                if r > b >> 1:
                    b = b - r
                else:
                    b = r
            return a

    def bezout_module(self, a: int, b: int) -> tuple[int, int, int]:
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

    def mcd_n_module(self, nlist: list[int]) -> int:
        """
        [Z] -> Z
        Devuelve el maximo comun divisor de los numeros de nlist
        """
        return nlist

    def bezout_n_module(self, nlist: list[int]) -> tuple[int, list[int]]:
        """
        [Z] -> (Z, [Z])
        Devuelve una tupla (d,x) donde d es el mcd de los coeficientes y x es una solucion particular
        de d = c1*x1 + c2*x2 + ... + cn*xn
        """
        return nlist

    def coprimos_module(self, a: int, b: int) -> bool:
        """
        Z x Z -> Bool
        Comprueba si dos numeros son coprimos
        """
        if (a | b) & 1 == 0:
            return False
        return self.mcd_module(a, b) == 1

    def potencia_mod_p_module(self, base: int, exp: int, p: int) -> int:
        """
        Z x Z x Z -> Z
        Devuelve base^exp mod p
        Raise an exception if exp < 0 and base is not invertible mod p
        """
        if exp < 0:
            base = self.inverso_mod_p_module(base, p)
            exp = -exp
        elif exp == 0:
            return 1
        elif exp == 1:
            return base
        potencia = 1
        bin_str = bin(exp)
        base = base % p
        for i in range(len(bin_str) - 1, 1, -1):
            if bin_str[i] == "1":
                potencia = (potencia * base) % p
            base = (base * base) % p
        return potencia

    def inverso_mod_p_module(self, n: int, p: int) -> int:
        """
        Z x Z -> Z
        Devuelve el inverso de n mod p
        Raise an exception if n is not invertible mod p
        """
        n = n % p
        a_comb = 1
        b_comb = 0
        while n:
            a_comb, b_comb = b_comb - a_comb * (p // n), a_comb
            p, n = n, p % n
        assert p != 1, f"{n} no tiene inversa mod {p} (NE)"
        return b_comb

    def euler_module(self, n: int) -> int:
        """
        Z -> Z
        Devuelve el valor de euler totient of n
        If n is negative, raise an exception ?
        """
        primos = self.factorizar_module(n).keys()
        tot = n
        for primo in primos:
            tot -= tot / primo
        return tot

    def legendre_module(self, n: int, p: int) -> int:
        """
        Z x Z -> Z
        Devuelve el simbolo de legendre de n y p
        """
        return self.potencia_mod_p_module(n, (p - 1) // 2, p)

    def resolver_sistema_congruencias_module(
        self, alist: list[int], blist: list[int], plist: list[int]
    ) -> tuple[int, list[int]]:
        """
        [Z] x [Z] x [Z] -> (Z, [Z])
        Resuelve el sistema de congruencias lineal y devuelve una tupla (r,m) donde r es la solucion modulo m
        """
        return alist, blist, plist

    def raiz_mod_p_module(self, n: int, p: int) -> int:
        """
        Z x Z -> Z (Tupla ?)
        Devuelve una raiz cuadrada de n mod p
        - Si n tiene dos raices distintas x1 < x2, las escribe en orden: “x1, x2”
        - Si n tiene una unica raiz x, escribe “x”
        - Si n no tiene raices, como con el resto de comandos, escribe “NE” en modo “batch” o un mensaje de error
        adecuado en modo interactivo.
        """
        return n, p

    def ecuacion_cuadratica_module(
        self, a: int, b: int, c: int, p: int
    ) -> tuple[int, int]:
        """
        Z x Z x Z x Z -> (Z, Z)
        Devuelve una solucion de la ecuacion ax^2 + bx + c = 0 mod p
        - Si la ecuacion tiene dos raices distintas x1 < x2, las escribe en orden: “x1, x2”
        - Si la ecuacion tiene una unica raiz doble x, escribe “x”
        - Si la ecuacion no tiene raices, como con el resto de comandos, escribe “NE” en modo “batch” o un mensaje de
        error adecuado en modo interactivo.
        """
        return a, b, c, p


if "imatlab_module" not in globals():
    imatlab_module = Module()


def es_primo(n: int) -> bool:
    """
    Z -> Bool
    Comprueba si un numero es primo
    """
    return imatlab_module.es_primo_module(n)


def factorizar(n: int) -> dict[int, int]:
    """
    Z -> {Z: Z}
    Devuelve el factorizacion de n
    """
    return imatlab_module.factorizar_module(n)


def mcd(a: int, b: int) -> int:
    """
    Z x Z -> Z
    Devuelve el maximo comun divisor de a y b
    """
    return imatlab_module.mcd_module(a, b)


def bezout(a: int, b: int) -> tuple[int, int, int]:
    """
    Z x Z -> (Z, Z, Z)
    Devuelve una tupla (d,x,y) donde d es el mcd de a y b y x,y son soluciones particulares de d = ax + by
    """
    return imatlab_module.bezout_module(a, b)


def coprimos(a: int, b: int) -> bool:
    """
    Z x Z -> Bool
    Comprueba si dos numeros son coprimos
    """
    return imatlab_module.coprimos_module(a, b)


def potencia_mod_p(base: int, exp: int, p: int) -> int:
    """
    Z x Z x Z -> Z
    Devuelve base^exp mod p
    Raise an exception if exp < 0 and base is not invertible mod p
    """
    return imatlab_module.potencia_mod_p_module(base, exp, p)


def inverso_mod_p(n: int, p: int) -> int:
    """
    Z x Z -> Z
    Devuelve el inverso de n mod p
    Raise an exception if n is not invertible mod p
    """
    return imatlab_module.inverso_mod_p_module(n, p)


def euler(n: int) -> int:
    """
    Z -> Z
    Devuelve el valor de euler totient of n
    If n is negative, raise an exception ?
    """
    return imatlab_module.euler_module(n)


def legendre(n: int, p: int) -> int:
    """
    Z x Z -> Z
    Devuelve el simbolo de legendre de n y p
    """
    return imatlab_module.legendre_module(n, p)


def resolver_sistema_congruencias(
    alist: list[int], blist: list[int], plist: list[int]
) -> tuple[int, list[int]]:
    """
    [Z] x [Z] x [Z] -> (Z, [Z])
    Resuelve el sistema de congruencias lineal y devuelve una tupla (r,m) donde r es la solucion modulo m
    """
    return imatlab_module.resolver_sistema_congruencias_module(alist, blist, plist)


def raiz_mod_p(n: int, p: int) -> int:
    """
    Z x Z -> Z (Tupla ?)
    Devuelve una raiz cuadrada de n mod p
    - Si n tiene dos raices distintas x1 < x2, las escribe en orden: “x1, x2”
    - Si n tiene una unica raiz x, escribe “x”
    - Si n no tiene raices, como con el resto de comandos, escribe “NE” en modo “batch” o un mensaje de error
    adecuado en modo interactivo.
    """
    return imatlab_module.raiz_mod_p_module(n, p)


if __name__ == "__main__":
    # print("es_primo:")
    # print(timeit.timeit("print(es_primo(383904623))", globals=globals(), number=1))
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
