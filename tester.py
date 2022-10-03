import modular
from imatlab import Imatlab
import sympy


def testPrimos():
    lab = Imatlab()
    with open("tests/primosTest.txt", "r") as f:
        for line in f:
            name, args = lab.parse_command(line)
            if name == "primo":
                assert sympy.isprime(args[0]) == modular.es_primo(args[0])
            elif name == "primos":
                assert modular.lista_primos(args[0], args[1]) == list(
                    sympy.primerange(args[0], args[1])
                )
    print("All tests passed")


def testSistema():
    lab = Imatlab()
    with open("tests/sistemaTest.txt", "r") as f:
        for line in f:
            name, args = lab.parse_command(line)
            if name == "resolverSistema":
                print(args)
                my_sol = lab.COMMANDS[name].execute(args)
                x = my_sol[0]
                assert all((a * x) % m == b for a, b, m in args[0])
    print("All tests passed")


testSistema()
