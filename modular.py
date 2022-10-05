import math
import numpy as np
import warnings

warnings.simplefilter("error", RuntimeWarning)


class Module:
    def __init__(self):
        self.cache = {}
        self.fp2 = Fp2(self.legendre_module)

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
        if a > 2:
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
        else:
            primos = []
            es_primo = [True] * (b + 1)
            for i in range(2, b + 1):
                if es_primo[i]:
                    primos.append(i)
                    for j in range(i * i, b + 1, i):
                        es_primo[j] = False
            return primos

    def factorizar_simple_module(self, n: int):
        """
        Returns the prime factors of n in a dictionary in O(sqrt(n))
        """
        factors = dict()
        for i in range(41, int(math.sqrt(n)) + 1, 2):
            while n % i == 0:
                n //= i
                factors[i] = factors.get(i, 0) + 1
            if n == 1:
                return factors
        return {n: 1}

    def factorizar_module(self, n: int) -> dict[int, int]:
        """
        Z -> {Z: Z, ...}
        Devuelve un diccionario con los factores primos de n y sus exponentes
        If n is 0 or 1, raise an exception ?
        """
        factors = dict()
        firsts = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
        for primo in firsts:
            while n % primo == 0:
                n //= primo
                factors[primo] = factors.get(primo, 0) + 1
        if n < 10**10:
            return {**factors, **self.factorizar_simple_module(n)}
        else:
            g = lambda x: (x**2 + 1) % n
            seed = 1
            while x < 5:
                seed += 1
                x = y = seed
                d = 1
                while d == 1:
                    x = g(x)
                    y = g(g(y))
                    d = self.mcd_simple_module((x - y) % n, n)
                if d != n:
                    return {
                        **factors,
                        **self.factorizar_module(d),
                        **self.factorizar_module(n // d),
                    }
            return {**factors, **self.factorizar_simple_module(n)}

    def mcd_simple_module(self, a: int, b: int) -> int:
        """
        Z x Z -> Z
        Devuelve el maximo comun divisor de a y b usando euclides
        """
        if a > b:
            a, b = b, a
        while b:
            a, b = b, a % b
        return a

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
                r, a = a % b, b
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

        return b, int(b_coeffs[0]), int(b_coeffs[1])

    def mcd_n_module(self, nlist: list[int]) -> int:
        """
        [Z] -> Z
        Devuelve el maximo comun divisor de los numeros de nlist
        """
        gcd = nlist.pop()
        for n in nlist:
            gcd = self.mcd_module(gcd, n)
            if gcd == 1:
                return 1
        return gcd

    def bezout_n_module(self, nlist: list[int]) -> tuple[int, list[int]]:
        """
        [Z] -> (Z, [Z])
        Devuelve una tupla (d,x) donde d es el mcd de los coeficientes y x es una solucion particular
        de d = c1*x1 + c2*x2 + ... + cn*xn
        """
        length = len(nlist)
        coeffs = [
            np.array([0] * i + [1] + [0] * (length - i - 1)) for i in range(length)
        ]
        i = 0
        count_zeros = 0
        while count_zeros != length - 1:
            m = nlist[i]
            if m == 0:
                i = (i + 1) % length
                continue
            count_zeros = 0
            for j in range(length):
                if i == j:
                    continue
                num = nlist[j]
                if num == 0:
                    count_zeros += 1
                    continue
                nlist[j] = num % m
                coeffs[j] -= coeffs[i] * (num // m)
                # print(nlist, list(coeffs))
            i = (i + 1) % length
        return m, list(coeffs[(i - 1) % length])

    def coprimos_module(self, a: int, b: int) -> bool:
        """
        Z x Z -> Bool
        Comprueba si dos numeros son coprimos.
        Mas rapido con mcd_simple.
        """
        if (a | b) & 1 == 0:
            return False
        return self.mcd_simple_module(a, b) == 1

    def potencia_mod_p_module(self, base: int, exp: int, p: int) -> int:
        """
        Z x Z x Z -> Z
        Devuelve base^exp mod p
        Raise an exception if exp < 0 and base is not invertible mod p
        """
        if exp < 0:
            base = self.inverso_mod_p_module(base, p)
            exp = -exp
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
        a, m = n % p, p
        a_coeff = 1
        b_coeff = 0
        while a:
            a_coeff, b_coeff = b_coeff - a_coeff * (m // a), a_coeff
            m, a = a, m % a
        assert m == 1, f"{n} no tiene inversa mod {p} (NE)"
        return b_coeff % p

    # def euler_module(self, n: int) -> int:
    #     """
    #     Z -> Z
    #     Devuelve el valor de euler totient of n
    #     If n is negative, raise an exception ?
    #     """
    #     primos = self.factorizar_module(n).keys()
    #     tot = n
    #     for primo in primos:
    #         tot -= tot // primo
    #     return tot

    def euler_module(self, n: int) -> int:
        """
        Z -> Z
        Devuelve el valor de euler totient of n
        If n is negative, raise an exception ?
        """
        tot = n
        firsts = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
        for primo in firsts:
            if n % primo == 0:
                tot -= tot // primo
                while n % primo == 0:
                    n = n // primo
                if n == 1:
                    return tot

        for i in range(41, int(n**0.5) + 1, 2):
            if n % i == 0:
                tot -= tot // i
                while n % i == 0:
                    n //= i
                if n == 1:
                    return tot
        return n - 1

    def legendre_module(self, n: int, p: int) -> int:
        """
        Z x Z -> Z
        Devuelve el simbolo de legendre de n y p
        """
        l = self.potencia_mod_p_module(n, (p - 1) // 2, p)
        if l not in (0, 1):
            return -1

    def resolver_sistema_congruencias_module2(
        self, alist: list[int], blist: list[int], plist: list[int]
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
            gcd = self.mcd_simple_module(self.mcd_simple_module(a, b), p)
            if gcd > 1:
                alist[k] = a // gcd
                blist[k] = b // gcd
                plist[k] = p // gcd
        m = 1
        for p in plist:
            m *= p
        x = 0
        for a, b, p in zip(alist, blist, plist):
            nk = m // p
            xk = self.inverso_mod_p_module(nk, p)
            a_inv = self.inverso_mod_p_module(a, p)
            x += nk * xk * a_inv
        return x % m, m

    def resolver_sistema_congruencias_module(
        self, alist: list[int], blist: list[int], plist: list[int]
    ) -> tuple[int, list[int]]:
        """
        [Z] x [Z] x [Z] -> (Z, [Z])
        Resuelve el sistema de congruencias lineal y devuelve una tupla (r,m) donde r es la solucion modulo m.
        Doc: https://forthright48.com/chinese-remainder-theorem-part-2-non-coprime-moduli/
        """
        size = len(plist)
        for k in range(size):
            a, b, p = alist[k], blist[k], plist[k]
            gcd = self.mcd_simple_module(self.mcd_simple_module(a, b), p)
            a, b, p = a // gcd, b // gcd, p // gcd
            alist[k], blist[k], plist[k] = 1, b * self.inverso_mod_p_module(a, p) % p, p
        for i in range(size - 2, -1, -1):
            a1, m1 = blist[i + 1], plist[i + 1]
            a2, m2 = blist[i], plist[i]
            g, p, q = self.bezout_module(m1, m2)
            assert (a1 - a2) % g == 0, "Cannot solve the system (NE)"
            blist[i] = (a1 * (m2 // g) * q + a2 * (m1 // g) * p) // g
            plist[i] = (m1 * m2) // g
        return blist[0] % plist[0], plist[0]

    def raiz_mod_p_module(self, n: int, p: int) -> int:
        """
        Z x Z -> Z (Tupla ?)
        Devuelve una raiz cuadrada de n mod p
        - Si n tiene dos raices distintas x1 < x2, las escribe en orden: “x1, x2”
        - Si n tiene una unica raiz x, escribe “x”
        - Si n no tiene raices, como con el resto de comandos, escribe “NE” en modo “batch” o un mensaje de error
        adecuado en modo interactivo.
        """
        if p == 2:
            return n % 2
        assert (
            self.legendre_module(n, p) != -1
        ), f"{n} no tiene raiz cuadrada mod {p} (NE)"
        if p % 4 == 3:
            return self.potencia_mod_p_module(n, (p + 1) // 4, p)
        elif p % 8 == 5:
            return self.potencia_mod_p_module(n, (p + 3) // 8, p)
        else:
            return self.fp2.sqrt(n, p)

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
        a, b, c = a % p, b % p, c % p
        sqrt = self.raiz_mod_p_module((b * b - 4 * a * c) % p, p)
        x1 = (-b + sqrt) * self.inverso_mod_p_module(2 * a, p)
        x2 = (-b - sqrt) * self.inverso_mod_p_module(2 * a, p)
        return x1 % p, x2 % p


class Fp2:
    def __init__(self, legendre):
        self.legendre = legendre

    def find_generator(self, n: int, p: int) -> int:
        l = 1
        a = 1
        while l != -1:
            a += 1
            l = self.legendre(a * a - n, p)
        self.a = a
        self.w2 = a * a - n

    # def add(self, x: tuple, y: tuple, p: int) -> tuple:
    #     return (x[0] + y[0]) % p, (x[1] + y[1]) % p

    # def sub(self, x: tuple, y: tuple, p: int) -> tuple:
    #     return (x[0] - y[0]) % p, (y[1] - y[1]) % p

    def mult(self, x: tuple, y: tuple, p: int) -> tuple:
        real = x[0] * y[0] + x[1] * y[1] * self.w2
        imag = x[0] * y[1] + x[1] * y[0]
        return real % p, imag % p

    def exp(self, x: tuple, exp: int, p: int) -> tuple:
        potencia = (1, 0)
        bin_str = bin(exp)
        base = x
        for i in range(len(bin_str) - 1, 1, -1):
            if bin_str[i] == "1":
                potencia = self.mult(potencia, base, p)
            base = self.mult(base, base, p)
        return potencia

    def sqrt(self, n: int, p: int) -> int:
        self.find_generator(n, p)
        return self.exp((self.a, 1), (p + 1) // 2, p)[0]


if "imatlab_module" not in globals():
    print("Initializing imatlab_module")
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


def mcd_n(nlist: list[int]) -> int:
    """
    [Z] -> Z
    Devuelve el maximo comun divisor de los elementos de la lista
    """
    return imatlab_module.mcd_n_module(nlist)


def bezout_n(nlist: list[int]) -> tuple[int, list[int]]:
    """
    [Z] -> (Z, [Z])
    Devuelve una tupla (d, x) donde d es el mcd de los elementos de la lista y x es una lista de soluciones particulares de
    d = x1 * n1 + x2 * n2 + ... + xn * nn
    """
    return imatlab_module.bezout_n_module(nlist)


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


def ecuacion_cuadratica(a: int, b: int, c: int, p: int) -> tuple[int, int]:
    """
    Z x Z x Z x Z -> (Z, Z)
    Devuelve las raices de la ecuacion ax^2 + bx + c = 0 mod p
    """
    return imatlab_module.ecuacion_cuadratica_module(a, b, c, p)


if __name__ == "__main__":
    # print(resolver_sistema_congruencias([6519037604], [8972153143], [1297334945]))
    print(bezout_n([37, 15, 12, 22, 91, 49, 101]))
