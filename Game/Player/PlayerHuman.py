from typing import Optional

from .Player import Player
from ..Input.InputConsole import InputConsole
from ..Board.Board import Board


class PlayerHuman(Player):
    """Implement a human player making moves through console.

    Args:
        name: string name of a player.
        phrases: list of strings that player 'says'
                 at random when making move.

    Attributes:
        Inherited from Player

    Methods:
        Inherited from Player
    """

    def __init__(self,
                 name: Optional[str] = None,
                 phrases: Optional[list[str]] = None):
        """Implement human player.

        Args:
            name: string name of a player.
            phrases: list of strings that player 'says'
                     at random when making move.

        Returns:
            None

        Raises:
            None
        """
        super().__init__(
            name=name,
            phrases=phrases,
            _input=InputConsole()
        )

    def move(self, board: Board):
        """Place a stone on the board.

        Args:
            board: A board class implementing the game functions.

        Returns:
            None

        Raises:
            None
        """
        super().move(board)
