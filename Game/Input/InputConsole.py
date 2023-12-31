from .Input import Input


class InputConsole(Input):
    """Implement taking an intger from the console."""

    def get_int(self) -> int:
        """Obtain integer value from the console - the user input.

        Args:
            None

        Returns:
            int: integer

        Raises:
            Exception: If int(input_str) function fails
        """
        in_val: str = input("Select column: ")
        try:
            return int(in_val)
        except Exception as e:
            print(
                ("Input: I am expecting a positive integer " +
                 "value between 0 and board.width-1, but not '"), in_val, "'")
            print(e)
            return self.get_int()
