import modular
from imatlab import Imatlab
import sympy
import re
import math


def testPrimos():
    lab = Imatlab()
    with open("tests/primosTest.txt", "r") as f:
        for line in f:
            name, args = lab.parse_command(line)
            if name == "primo":
                print("Checking", args)
                assert sympy.isprime(int(args[0])) == modular.es_primo(int(args[0]))
            elif name == "primos":
                args = [int(a) for a in args.split(",")]
                assert modular.lista_primos(args[0], args[1]) == list(
                    sympy.primerange(args[0], args[1])
                )
            # elif name == "coprimos":
            #     args = [int(a) for a in args.split(",")]
            #     assert modular.coprimos(args[0]) == list(sympy.totientrange(args[0]))
    print("All tests passed")


def testFactorizar():
    with open("tests/factorTest.txt", "r") as ft:
        with open("tests/factorOut.txt", "r") as fo:
            for test, out in zip(ft, fo):
                n = int(re.search(r"\(([0-9]+)\)", test.strip()).group(1))
                out = eval("{" + out.strip() + "}")
                s = 1
                for p, e in out.items():
                    s *= p**e
                print(n, s)
                assert s == n
    print("All tests passed")


def testMCD():
    lab = Imatlab()
    with open("tests/mcdTest.txt", "r") as f:
        for line in f:
            name, args = lab.parse_command(line)
            if name == "mcd":
                x = lab.COMMANDS[name].execute(args)
                print(x, [int(a) for a in args.split(",")])
                assert x != math.gcd(*[int(a) for a in args.split(",")])
            else:
                print("WHAT")
                return
    print("All tests passed")


def testSistema():
    lab = Imatlab()
    with open("tests/sistemaTest.txt", "r") as f:
        for line in f:
            name, args = lab.parse_command(line)
            if name == "resolverSistema":
                try:
                    my_sol = lab.COMMANDS[name].execute(args)
                except Exception as e:
                    print(e, args)
                x = int(my_sol.split(" ")[0])
                print(args, x)
                assert all((arg[0] * x) % arg[2] == arg[1] for arg in args)
    print("All tests passed")


def testCuadratica():
    lab = Imatlab()
    with open("tests/cuadraticaTest.txt", "r") as f:
        for line in f:
            name, args = lab.parse_command(line)
            if name == "ecCuadratica":
                try:
                    my_sol = lab.COMMANDS[name].execute(args)
                    args = [int(a) for a in args.split(",")]
                    x1, x2 = [int(x) for x in my_sol.split(",")]
                    assert (args[0] * x1**2 + args[1] * x1 + args[2]) % args[3] == 0
                    assert (args[0] * x2**2 + args[1] * x2 + args[2]) % args[3] == 0
                    print(x1, x2, "Both solutions are correct")
                except Exception as e:
                    e = str(e)
                    n, p = int(e.split(" ")[0]), int(e.split(" ")[-1])
                    assert lab.COMMANDS["legendre"].execute(f"{n},{p}") == "-1"
                    print(n, p, "Legendre symbol is correct")
    print("All tests passed")


# testPrimos()
# testFactorizar()
# testMCD()
# testSistema()
# testFactorizar()
testCuadratica()
