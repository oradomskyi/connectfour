from random import randint

from .Input import Input


class InputAlgoRandom(Input):
    """Implement generating random an integer."""

    def __init__(self, n: int):
        """Instantiate random integer input generator.

        Args:
            n: number of integers to choose from,
               later integer will be chosen from {0 .. n-1}.

        Returns:
            None

        Raises:
            None
        """
        # -1 is necessary because board width,
        # but trated as index in 0-indexed list
        self.n = n-1

    def get_int(self) -> int:
        """Get integer from 0 to n-1.

        Args:
            None
        Returns:
            int: integer value taken from range{0..n-1}

        Raises:
            None
        """
        return randint(0, self.n)
