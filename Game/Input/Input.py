from .InputInterface import InputInterface


class Input(InputInterface):
    """Base class for inputs."""

    def get_int(self) -> int:
        """Ger intereger value from input.

        Abstract method to be implemented in subclasses.

        Args:
            None

        Returns:
            int: integer input value

        Raises:
            NotImplementedError: In case users did not proved implementation
                                 and calling the base class method
        """
        raise NotImplementedError
