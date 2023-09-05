from typing import Optional

from time import sleep
from random import randint

from .Player import Player
from ..Input.InputAlgoRandom import InputAlgoRandom
from ..Board.Board import Board


class PlayerAlgoRandom(Player):
    """Implement a 'computer' player making random moves.

    Args:
        n_moves: number of possible moves from range {0 .. n_moves}.
        name: string name of a player

    Attributes:
        Inherited from Player

    Methods:
        Inherited from Player
    """

    def __init__(self, n_moves: int, name: Optional[str] = None):
        """Initialize the random 'compiuter' player.

        Args:
            n_moves: number of possible moves from range {0 .. n_moves}.
            name: string name of a player

        Returns:
            None

        Raises:
            None
        """
        super().__init__(
            name=name,
            phrases=None,
            _input=InputAlgoRandom(n_moves)
        )

    def move(self, board: Board):
        """Place the stone

        Args:
            board: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """
        # some delay of 0 to 1000ms to make algo feel like 'making a decision'
        sleep(randint(0, 100) / 100)
        super().move(board)
