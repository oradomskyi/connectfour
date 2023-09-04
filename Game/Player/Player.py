from typing import Optional

from random import choice, randint
from string import ascii_lowercase

from ..Board.Board import Board


class Player:
    """Implement functions common for PlayerHuman and PlayerAlgoRandom.

    Attributes:
        _input: Interface to obtain user's input.
        symbol: A unique character representing 'stone color'.
        phrases: List[str] of what could be printed when player moves.
        ID: Unique int value from 0 to 41 that determines 'color'
            of the 'stone'.
        name: String containing player's name

    Methods:
        move(board): To set a stone on a board.
        __str__(): To serialize the class for printing outputs to the console.
        generate_random_name(): generator of a random name.
        set_ID(id: int): Set player ID.
        get_ID(): Get player ID.
        set_name(name: str): Set player name.
        get_name(): Get player name.
    """

    def __init__(self,
                 name: Optional[str] = None,
                 phrases: Optional[list[str]] = None,
                 _input=None):
        """Initialize an instance of a Player base class.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """
        self.input = _input
        self.symbol = None
        self.phrases = phrases
        self.ID = -1

        if name is None:
            self.name = self._generate_random_name()
        else:
            self.name = name

    def __str__(self) -> str:
        """Constructor
        prepares the list of symbols(colors) that could be used for different
        players by default there could be up to 42 players. Also initializes
        the board matrix, column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """
        about = "\nPlayer " + self.name

        if self.ID is not None:
            about += " #" + str(self.ID) + " "

        if self.phrases is not None:
            about += " '" + choice(self.phrases) + "'"
        return about

    def _generate_random_name(self) -> str:
        """Generate a random name of 1 to 10 of small ASCII characters.

        Args:
            None

        Returns:
            name: Random name string

        Raises:
            None
        """
        name_length = randint(1, 10)
        letters = ascii_lowercase
        name = ''.join(choice(letters) for i in range(name_length))
        return name

    def set_ID(self, _id: int):
        """Set player ID.

        Args:
            _id: Integer value between 0 and 41

        Returns:
            None

        Raises:
            None
        """
        self.ID = _id

    def get_ID(self) -> int:
        """Get player ID.

        Args:
            None

        Returns:
            ID: Integer value between 0 and 41

        Raises:
            None
        """
        return self.ID

    def get_name(self) -> str:
        """Get player Name.

        Args:
            None

        Returns:
            name: string with player name

        Raises:
            None
        """
        return self.name

    def set_name(self, name: str):
        """Set player name.

        Args:
            name: string with player name

        Returns:
            None

        Raises:
            None
        """
        self.name = name

    def move(self, board: Board):
        """Place a stone on the board.

        Args:
            board: A board class implementing the game functions.

        Returns:
            None

        Raises:
            None
        """
        # Attempt to get player input
        column = self.input.get_int()

        # Attempt to place a stone
        try:
            board.apply(column, self.ID, self.name)
        except Exception as e:
            print(
                "Cannot play column",
                column,
                "it should be integer between 0 and",
                board.get_width()-1
            )

            print(e)
            self.move(board)