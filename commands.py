class Command:
    def __init__(self, function):
        # Function of the arithmetic module to be executed
        self.function = function

    def check_args(self, args: list) -> bool:
        """
        Checks if the arguments are valid.
        """
        return isinstance(args, list)

    def parse_args(self, args: list) -> list:
        """
        Parses the arguments to the correct type.
        """
        return args

    def parse_output(self, output) -> str:
        """
        Parses the output to a string.
        """
        return str(output)

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


class EsPrimo(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list) -> bool:
        return len(args) == 1 and isinstance(args[0], int)

    def parse_output(self, output) -> str:
        return "Sí" if output else "No"


class ListaPrimos(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list) -> bool:
        return len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int)

    def parse_output(self, output) -> str:
        return ", ".join([str(x) for x in output])


class Factorizar(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list) -> bool:
        return len(args) == 1 and isinstance(args[0], int)

    def parse_output(self, output) -> str:
        return ", ".join([f"{x}:{output[x]}" for x in output])


class MCD(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list) -> bool:
        for arg in args:
            if not isinstance(arg, int):
                return False
        return True


class Bezout(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list) -> bool:
        for arg in args:
            if not isinstance(arg, int):
                return False
        return True

    def parse_output(self, output) -> str:
        return f"{output[0]}, {output[1]}"


class Coprimos(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list) -> bool:
        return len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int)

    def parse_output(self, output) -> str:
        return "Sí" if output else "No"


class PotenciaModP(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list) -> bool:
        return (
            len(args) == 3
            and isinstance(args[0], int)
            and isinstance(args[1], int)
            and isinstance(args[2], int)
        )


class InversoModP(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list) -> bool:
        return len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int)


class Euler(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list) -> bool:
        return len(args) == 1 and isinstance(args[0], int)


class Legendre(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list) -> bool:
        return len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int)


class ResolverSistema(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list[list[int]]) -> bool:
        for arg in args:
            if not isinstance(arg, list) or len(arg) != 3:
                return False
            for x in arg:
                if not isinstance(x, int):
                    return False
        return True

    def parse_args(self, args: list[list[int]]) -> list[list[int]]:
        return [x[0] for x in args], [x[1] for x in args], [x[2] for x in args]


class RaizModP(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list) -> bool:
        return len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int)


class EcuacionCuadratica(Command):
    def __init__(self, function):
        super().__init__(function)

    def check_args(self, args: list) -> bool:
        return (
            len(args) == 4
            and isinstance(args[0], int)
            and isinstance(args[1], int)
            and isinstance(args[2], int)
            and isinstance(args[3], int)
        )

    def parse_output(self, output) -> str:
        x1, x2 = output
        if x1 == x2:
            return f"{x1}"
        if x1 > x2:
            return f"{x2}, {x1}"
        return f"{x1}, {x2}"
