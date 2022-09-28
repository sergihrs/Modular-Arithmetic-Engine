import sys
import os
from commands import COMMANDS


class Imatlab:
    def __init__(self):
        pass

    def parse_command(self, raw_input: str) -> tuple[str, list]:
        """
        Recieves raw input from user and returns a tuple with the name of the command
        and a list with the arguments.
        """
        raw_input = raw_input.strip()
        first_paren = raw_input.index("(")
        func = raw_input[:first_paren]
        args = raw_input[first_paren + 1 : -1].split(",")
        parsed_args = []
        for arg in args:
            if arg[0] == "[":
                parsed_args.append([int(x) for x in arg[1:-1].split(";")])
            else:
                parsed_args.append(int(arg))
        return func, parsed_args

    def execute_command(self, raw_input: str) -> str:
        """
        Recieves raw input command, converts it to a name and args and executes it.
        Returns output as a string.
        Controls possible errors.
        """
        try:
            name, args = self.parse_command(raw_input)
        except:
            raise ValueError("Error: Invalid input (NOP)")

        if name not in COMMANDS:
            raise ValueError(f"Error: Invalid command '{name}' (NOP)")

        output = COMMANDS[name].execute(args)

        return output

    def start_interface(self):
        try:
            raw_input = input(">>> ")
        except KeyboardInterrupt:
            return
        while raw_input.strip() not in ["exit", "quit", ""]:
            try:
                print(self.execute_command(raw_input))
            except Exception as e:
                print(e)
            try:
                raw_input = input(">>> ")
            except KeyboardInterrupt:
                return

    def run_batch(self, fin: str, fout: str):
        if not os.path.isfile(fin):
            print(f"Error: File '{fin}' not found")
        output = ""
        try:
            with open(fin, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        output += self.execute_command(line) + "\n"
                    except Exception as e:
                        output += str(e) + "\n"
        except Exception as e:
            print(e)
        try:
            with open(fout, "w", encoding="utf-8") as f:
                f.write(output)
        except:
            print(f"Error: Could not write to file '{fout}'")


def run_commands(fin, fout):
    """
    fin: TextIO
    fout: TextIO
    """
    imatlab = Imatlab()
    output = ""
    for line in fin:
        try:
            output += imatlab.execute_command(line) + "\n"
        except Exception as e:
            output += str(e) + "\n"
    fout.write(output)


if __name__ == "__main__":
    imatlab = Imatlab()
    if len(sys.argv) == 1:
        imatlab.start_interface()
    elif len(sys.argv) == 2:
        print("Error: Missing one argument")
    elif len(sys.argv) == 3:
        imatlab.run_batch(sys.argv[1], sys.argv[2])
    else:
        print("Error: Too many arguments")
