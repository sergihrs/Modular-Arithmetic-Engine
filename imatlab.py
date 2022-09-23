import modular
import re
import os
import sys

COMMANDS = {
    "primo": {"arg_types": [int], "function": modular.es_primo},
    "primos": {"arg_types": [int, int], "function": modular.lista_primos},
    "factorizar": {"arg_types": [int], "function": modular.factorizar},
    "mcd": {"arg_types": [int, int], "function": modular.mcd},
    "coprimos": {"arg_types": [int, int], "function": modular.coprimos},
    "pow": {"arg_types": [int, int, int], "function": modular.potencia_mod_p},
    "inv": {"arg_types": [int, int], "function": modular.inverso_mod_p},
    "euler": {"arg_types": [int], "function": modular.euler},
    "legendre": {"arg_types": [int, int], "function": modular.legendre},
    "resolverSistema": {
        "arg_types": list,
        "list_types": [int, int, int],
        "function": modular.resolver_sistema_congruencias,
    },
    "raiz": {"arg_types": [int, int], "function": modular.raiz_mod_p},
    "ecCuadratica": {
        "arg_types": [int, int, int, int],
        "function": modular.ecuacion_cuadratica,
    },
}


def parse_input(raw_input: str) -> tuple[str, list]:
    """
    Recieves raw input from user and returns a tuple with the name of the command
    and a list with the arguments.
    """
    raw_input = re.sub(r"\s+", "", raw_input)
    raw_input = re.sub(r";", ",", raw_input)
    name = re.search(r"(\w+)\(", raw_input).group(1)
    args = eval(re.search(r"\((.*)\)", raw_input).group(1))
    return name, args if isinstance(args, tuple) else [args]


def check_args(args, command):
    if type(command["arg_types"]) == list:
        if len(args) != len(command["arg_types"]):
            raise ValueError(
                f"Error: Invalid number of arguments. Expected {len(args)}, got {len(command['arg_types'])}"
            )
        for i, arg in enumerate(args):
            if type(arg) != command["arg_types"][i]:
                raise ValueError("Error: Invalid argument type")
    else:
        for i, arg in enumerate(args):
            if type(arg) != command["arg_types"]:
                raise ValueError("Error: Invalid argument type")
            if type(arg) == list:
                if len(arg) != len(command["list_types"]):
                    raise ValueError(
                        f"Error: Invalid number of arguments. Expected {len(arg)}, got {len(command['list_types'])}"
                    )
                for j, a in enumerate(arg):
                    if type(a) != command["list_types"][j]:
                        raise ValueError("Error: Invalid argument type")


def execute(raw_input: str) -> str:
    """
    Recieves raw input from user, converts it to a command and executes it.
    Returns output as a string.
    Controls possible errors.
    """
    try:
        name, args = parse_input(raw_input)
    except:
        raise ValueError(
            "Error: Invalid input. Must be of the form: command(arg1, arg2, ...)"
        )

    if name not in COMMANDS:
        raise ValueError(f"Error: Invalid command '{name}'")

    check_args(args, COMMANDS[name])

    if name == "resolverSistema":
        args = [
            [args[i][0] for i in range(len(args))],
            [args[i][1] for i in range(len(args))],
            [args[i][2] for i in range(len(args))],
        ]

    return str(COMMANDS[name]["function"](*args))


def interface():
    try:
        raw_input = input(">>> ")
    except KeyboardInterrupt:
        return
    while raw_input.strip() not in ["exit", "quit"]:
        if raw_input.strip() in ["clear", "cls"]:
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")
        else:
            try:
                print(execute(raw_input))
            except Exception as e:
                print(e)
        try:
            raw_input = input(">>> ")
        except KeyboardInterrupt:
            return


def execute_file(fin: str, fout: str):
    if not os.path.isfile(fin):
        raise FileNotFoundError(f"Error: File '{fin}' not found")
    output = ""
    with open(fin, "r") as f:
        for line in f:
            try:
                output += execute(line) + "\n"
            except Exception as e:
                output += str(e) + "\n"
    try:
        with open(fout, "w") as f:
            f.write(output)
    except:
        raise PermissionError(f"Error: Could not write to file '{fout}'")


def batch(fin: str, fout: str):
    try:
        execute_file(fin, fout)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        interface()
    elif len(sys.argv) == 2:
        print("Error: Missing one argument")
    elif len(sys.argv) == 3:
        batch(sys.argv[1], sys.argv[2])
    else:
        print("Error: Too many arguments")
