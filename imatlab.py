import modular
import re
import os
import sys


class Command:
    def __init__(
        self,
        name,
        function,
        check_args=lambda args: True,
        parse_args=lambda args: args,
        parse_output=lambda output: str(output),
    ):
        # The name of the command
        self.name = name
        # The function to execute
        self.function = function
        # A function to check if the arguments are valid
        self.check_args = check_args
        # A function to parse the arguments
        self.parse_args = parse_args
        # A function to parse the output
        self.parse_output = parse_output

    def execute(self, args: list):
        # Raise an exception if the arguments are not valid
        if not self.check_args(args):
            raise ValueError("Error: Invalid arguments (NOP)")
        # Parse the arguments
        parsed_args = self.parse_args(args)
        # Execute the function
        output = self.function(*parsed_args)
        # Parse the output
        return self.parse_output(output)


COMMANDS = {
    "primo": Command(
        name="primo",
        function=modular.es_primo,
        check_args=lambda args: (len(args) == 1 and type(args[0]) == int),
        parse_output=lambda output: "Sí" if output else "No",
    ),
    "primos": Command(
        name="primos",
        function=modular.lista_primos,
        check_args=lambda args: len(args) == 2
        and all(type(arg) == int for arg in args),
        parse_output=lambda output: ", ".join(map(str, output)),
    ),
    "factorizar": Command(
        name="factorizar",
        function=modular.factorizar,
        check_args=lambda args: len(args) == 1 and type(args[0]) == int,
        parse_output=lambda output: ", ".join(
            map(lambda x: f"{x[0]}:{x[1]}", output.items())
        ),
    ),
    "mcd": Command(
        name="mcd",
        function=modular.mcd,
        check_args=lambda args: len(args) >= 2
        and all(type(arg) == int for arg in args),
    ),
    "coprimos": Command(
        name="coprimos",
        function=modular.coprimos,
        check_args=lambda args: len(args) == 2
        and all(type(arg) == int for arg in args),
        parse_output=lambda output: "Sí" if output else "No",
    ),
    "pow": Command(
        name="pow",
        function=modular.potencia_mod_p,
        check_args=lambda args: len(args) == 3
        and all(type(arg) == int for arg in args),
    ),
    "inv": Command(
        name="inv",
        function=modular.inverso_mod_p,
        check_args=lambda args: len(args) == 2
        and all(type(arg) == int for arg in args),
    ),
    "euler": Command(
        name="euler",
        function=modular.euler,
        check_args=lambda args: len(args) == 1 and type(args[0]) == int,
    ),
    "legendre": Command(
        name="legendre",
        function=modular.legendre,
        check_args=lambda args: len(args) == 2
        and all(type(arg) == int for arg in args),
    ),
    "resolverSistema": Command(
        name="resolverSistema",
        function=modular.resolver_sistema_congruencias,
        check_args=lambda args: all(
            type(arg) == list and len(arg) == 3 and all(type(a) == int for a in arg)
            for arg in args
        ),
        parse_args=lambda args: [
            [args[i][0] for i in range(len(args))],
            [args[i][1] for i in range(len(args))],
            [args[i][2] for i in range(len(args))],
        ],
        parse_output=lambda output: f"{output[0]} (mod {output[1]})",
    ),
    "raiz": Command(
        name="raiz",
        function=modular.raiz_mod_p,
        check_args=lambda args: len(args) == 2
        and all(type(arg) == int for arg in args),
        parse_output=lambda output: str(output[0])
        if output[0] == output[1]
        else f"{min(output)}, {max(output)}",
    ),
    "ecCuadratica": Command(
        name="ecCuadratica",
        function=modular.ecuacion_cuadratica,
        check_args=lambda args: len(args) == 4
        and all(type(arg) == int for arg in args),
        parse_output=lambda output: str(output[0])
        if output[0] == output[1]
        else f"{min(output)}, {max(output)}",
    ),
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


def execute(raw_input: str) -> str:
    """
    Recieves raw input from user, converts it to a command and executes it.
    Returns output as a string.
    Controls possible errors.
    """
    try:
        name, args = parse_input(raw_input)
    except:
        raise ValueError("Error: Invalid input (NOP)")

    if name not in COMMANDS:
        raise ValueError(f"Error: Invalid command '{name}' (NOP)")

    output = COMMANDS[name].execute(args)

    return output


def interface():
    try:
        raw_input = input(">>> ")
    except KeyboardInterrupt:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        return
    while raw_input.strip() not in ["exit", "quit", ""]:
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
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")
            return
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def execute_file(fin: str, fout: str):
    if not os.path.isfile(fin):
        raise FileNotFoundError(f"Error: File '{fin}' not found")
    output = ""
    with open(fin, "r") as f:
        for line in f:
            try:
                output += execute(line) + "\n"
            except Exception as e:
                output += "NOP" + "\n"
    try:
        with open(fout, "w") as f:
            f.write(output)
    except:
        raise PermissionError(f"Error: Could not write to file '{fout}'")


def run_commands(fin, fout):
    """
    fin: TextIO
    fout: TextIO
    """
    output = ""
    for line in fin:
        try:
            output += execute(line) + "\n"
        except Exception as e:
            output += str(e) + "NOP" + "\n"
    fout.write(output)


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
