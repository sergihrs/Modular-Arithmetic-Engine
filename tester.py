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


testPrimos()
