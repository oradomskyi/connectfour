from ..Board.Board import Board


class PlayerInterface:
    """An abstract interface class providing a definition
    of how users would interact with Player class when implementing these.
    """

    def move(self, board: Board):
        """Set a 'stone' on a board.

        Args:
            board: A board class implementing the game functions.

        Returns:
            None

        Raises:
            NotImplementedError: If user tries to call an abstract method.
        """
        raise NotImplementedError
