import modular


class Command:
    def __init__(
        self,
        function,
        check_args=lambda args: True,
        parse_args=lambda args: args,
        parse_output=lambda output: str(output),
    ):
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
        try:
            output = self.function(*parsed_args)
        except Exception as e:
            raise ValueError(f"Error: {e}")
        # Parse the output
        return self.parse_output(output)


COMMANDS = {
    "primo": Command(
        function=modular.es_primo,
        check_args=lambda args: (len(args) == 1 and type(args[0]) == int),
        parse_output=lambda output: "Sí" if output else "No",
    ),
    "primos": Command(
        function=modular.lista_primos,
        check_args=lambda args: len(args) == 2
        and all(type(arg) == int for arg in args),
        parse_output=lambda output: ", ".join(map(str, output)),
    ),
    "factorizar": Command(
        function=modular.factorizar,
        check_args=lambda args: len(args) == 1 and type(args[0]) == int,
        parse_output=lambda output: ", ".join(
            map(lambda x: f"{x[0]}:{x[1]}", output.items())
        ),
    ),
    "mcd": Command(
        function=modular.mcd,
        check_args=lambda args: len(args) >= 2
        and all(type(arg) == int for arg in args),
    ),
    "coprimos": Command(
        function=modular.coprimos,
        check_args=lambda args: len(args) == 2
        and all(type(arg) == int for arg in args),
        parse_output=lambda output: "Sí" if output else "No",
    ),
    "pow": Command(
        function=modular.potencia_mod_p,
        check_args=lambda args: len(args) == 3
        and all(type(arg) == int for arg in args),
    ),
    "inv": Command(
        function=modular.inverso_mod_p,
        check_args=lambda args: len(args) == 2
        and all(type(arg) == int for arg in args),
    ),
    "euler": Command(
        function=modular.euler,
        check_args=lambda args: len(args) == 1 and type(args[0]) == int,
    ),
    "legendre": Command(
        function=modular.legendre,
        check_args=lambda args: len(args) == 2
        and all(type(arg) == int for arg in args),
    ),
    "resolverSistema": Command(
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
        function=modular.raiz_mod_p,
        check_args=lambda args: len(args) == 2
        and all(type(arg) == int for arg in args),
        parse_output=lambda output: str(output[0])
        if output[0] == output[1]
        else f"{min(output)}, {max(output)}",
    ),
    "ecCuadratica": Command(
        function=modular.ecuacion_cuadratica,
        check_args=lambda args: len(args) == 4
        and all(type(arg) == int for arg in args),
        parse_output=lambda output: str(output[0])
        if output[0] == output[1]
        else f"{min(output)}, {max(output)}",
    ),
}
