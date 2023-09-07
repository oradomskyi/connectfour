from random import choice, randint
from warnings import warn


class Board:
    """The logic of the "Connect Four" game
        with output to the console.

        By default there could be up to 42 players. Initializes the board
        matrix, column height counter and other internal variables.

        Args:
            width: width of the gaming board, expected to be positive
                   integer greater than zero.
            height: height of the gaming board, expected to be positive
                   integer greater than zero.
            line_length: line_length of the gaming board, expected to be
                         a positive integer greater than zero.
    """

    def __init__(self, width: int, height: int, line_length: int):
        """Prepares the list of SYMBOLS(colors) that could be used for players.

        By default there could be up to 42 players. Initializes the board
        matrix, column height counter and other internal variables.

        Args:
            width: width of the gaming board, expected to be positive
                   integer greater than zero.
            height: height of the gaming board, expected to be positive
                   integer greater than zero.
            line_length: line_length of the gaming board, expected to be
                         a positive integer greater than zero.

        Returns:
            None

        Raises:
            ValueError: If width is negative.
            ValueError: If height is negative.
            ValueError: If line_length is negative, greater than board width
                        or greater than the board height.
        """

        # https://en.wikipedia.org/wiki/Geometric_Shapes_(Unicode_block)
        self.N_SYMBOLS: int = 42
        self.SYMBOLS_START: int = ord("\u25b0")
        self.SYMBOLS: list[str] = [
            chr(self.SYMBOLS_START + i) for i in range(0, self.N_SYMBOLS)
        ]

        print("\n\nBoard says:\nI have", self.N_SYMBOLS,
              "stones:", self.SYMBOLS)

        self.i_symbol: int = 0
        self.EMPTY_SYMBOL: str = ' '
        self.solved: bool = False
        self.empty_cells_left: int = width*height
        self.player_moves: list[int] = []  # this would keep moves - their IDs

        # Let's dive into initializaton...
        if 0 < width:
            self.width: int = width
        else:
            raise ValueError(
                "I am not sure how play on a Board of width", width)

        if 0 < height:
            self.height: int = height
        else:
            raise ValueError(
                "I am not sure how play on a Board of height", height)

        if 0 < line_length:
            if line_length <= self.width and line_length <= self.height:
                self.line_length: int = line_length
            else:
                raise ValueError("Line sould be no longer than board ",
                                 "width of ", self.width,
                                 "or height of ", self.height,
                                 ", and not", line_length)
        else:
            raise ValueError(
                "Line length should be greater than zero and not", line_length)

        # Create a matrix for storing state of the game
        self.board: list[list[str]] = [
            [
                self.EMPTY_SYMBOL for i in range(0, self.width)
            ] for j in range(0, self.height)
        ]

        # Create indexing for the columns
        self.columns_height: list[int] = [0 for i in range(0, self.width)]

    def __str__(self) -> str:
        """Serialize the board matrix.

        Args:
            None

        Returns:
            str: string representation of the board
                 for printing out to the console

        Raises:
            None
        """

        text: str = "\n\n"

        # DEC column indices do not fit when there are more than 10 columns
        # HEX when there amore than 16...
        # But I see no clear reason of making the field printout wider
        if self.width <= 16:
            text += " "
            for i in range(0, self.width):
                text += "{:01x}".format(i) + " "

        text += "\n\n"
        for row in self.board:
            text += "|"
            for cell in row:
                text += cell+"|"

            text += "\n"

        text += "\n"

        return text

    def next_unused_stone(self) -> int:
        """Get the index of the next unused stone.

        Args:
            None

        Returns:
            int: index of the unused stone.

        Raises:
            Exception: If no available unused stones left.
        """

        if self.i_symbol == self.N_SYMBOLS:
            raise Exception(
                "Board says: Wow-wow, I do not have capacity for more than",
                self.N_SYMBOLS,
                "players!")

        self.i_symbol += 1
        return self.i_symbol-1

    def get_symbol(self, i_symbol: int) -> str:
        """Map player ID to the character of the player's stone.

        Args:
            i_symbol: player ID, or index of the stone

        Returns:
            str: string with the stone character

        Raises:
            ValueError: If ID is negative or greater than the number of stones.
        """

        if i_symbol < 0 or self.N_SYMBOLS <= i_symbol:
            raise ValueError(
                "Player ID sould be an integer from 0 to ", self.N_SYMBOLS-1,
                ", and not", i_symbol)

        return self.SYMBOLS[i_symbol]

    def get_width(self) -> int:
        """Get the board width.

        Args:
            None

        Returns:
            int: width of the board.

        Raises:
            None
        """
        return self.width

    def _limit_top(self,
                   i_stone: int,
                   j_stone: int,
                   i_cell: int,
                   j_cell: int) -> bool:
        """Test if i_cell is within the board and
           within the distance of line_length UP from i_stone.

        Args:
            i_stone: vertical position of the stone
            j_stone: horizontal position of the stone
            i_cell: vertical index if cell to test
            j_cell: horizontal index if cell to test

        Returns:
            bool: True when di within the allowed range.

        Raises:
            None
        """
        return (i_cell < 0) or (i_cell < i_stone - self.line_length)

    def _limit_bottom(self,
                      i_stone: int,
                      j_stone: int,
                      i_cell: int,
                      j_cell: int) -> bool:
        """Test if i_cell is within the board and
           within the distance of line_length DOWN from i_stone.

        Args:
            i_stone: vertical position of the stone
            j_stone: horizontal position of the stone
            i_cell: vertical index if cell to test
            j_cell: horizontal index if cell to test

        Returns:
            bool: True when di within the allowed range.

        Raises:
            None
        """
        return (self.height <= i_cell) or (i_stone+self.line_length < i_cell)

    def _limit_left(self,
                    i_stone: int,
                    j_stone: int,
                    i_cell: int,
                    j_cell: int) -> bool:
        """Test if j_cell is within the board and
           within the distance of line_length LEFTWARD from j_stone.

        Args:
            i_stone: vertical position of the stone
            j_stone: horizontal position of the stone
            i_cell: vertical index if cell to test
            j_cell: horizontal index if cell to test

        Returns:
            bool: True when j_cell within the allowed range.

        Raises:
            None
        """
        return (j_cell < 0) or (j_cell < j_stone - self.line_length)

    def _limit_right(self,
                     i_stone: int,
                     j_stone: int,
                     i_cell: int,
                     j_cell: int) -> bool:
        """Test if j_cell is within the board and
           within the distance of line_length RIGHTWARD from j_stone.

        Args:
            i_stone: vertical position of the stone
            j_stone: horizontal position of the stone
            i_cell: vertical index if cell to test
            j_cell: horizontal index if cell to test

        Returns:
            bool: True when j_cell within the allowed range.

        Raises:
            None
        """
        return (self.width <= j_cell) or (j_stone + self.line_length < j_cell)

    def _check(self, column: int) -> bool:
        """Check if player can place a stone in a given column
           and if it result in winning the game.

           In particular, given index of column where to place the stone
           first see if column is not full and place the stone if not,
           and then starting from position [i][j] of where the sone ended up
           count similar stones verticaly, then horizontaly, on main
           and secondary diagonals, going not further than the line_length.

           Also not checking any stones right above the current stone,
           as there is no possibility for any other stones to be - current
           stone always the topmost.

        Args:
            column: index of a column where to put the stone.

        Returns:
            True if stone is successfully placed.

        Raises:
            None
        """

        # print(self.empty_cells_left)
        if self.empty_cells_left == 0:
            return False

        # I do not know if there is any efficient way to test the board,
        # maybe it is not that bad to spawn recursion from the last move
        # in order not to re-compute entire board all over again..
        # but still - multiple cells would be evalated multiple times.

        # Get the last move location and symbol
        i: int = self.height - self.columns_height[column]
        j: int = column
        symbol: str = self.board[i][j]

        '''
        # this may help other player to pay attention, which is not ideal...
        print("Last Move:", i, j, symbol)
        '''

        # We will test vertical, horizontal and
        # two diagonals passing throught the
        # cell of the last move for existense
        # of a continuous line of at least self.line_length

        # -- Check cells Up and Down from current if there is a continuous line
        # in the range i={-L, -L+1, .., 0, .., L-1, L} where L=line_length

        # Actually, situation when there are values
        # in the column above the last move is not possible,
        # so I leave it here for my reference
        '''
        score_up = -1 # not 0 because current cell will be counted
        i_cell = i
        j_cell = j
        while ((not self._limit_top(i, j, i_cell, j_cell)) and
               (symbol in self.board[i_cell][j_cell])):
            score_up += 1
            i_cell -= 1
        '''
        score_up: int = 0

        score_down: int = -1
        i_cell = i
        j_cell = j
        while ((not self._limit_bottom(i, j, i_cell, j_cell)) and
               (symbol in self.board[i_cell][j_cell])):
            score_down += 1
            i_cell += 1

        score_vertical: int = score_up + score_down + 1

        # -- Now let's do the same horizontaly
        score_left = -1  # not 0 because current cell will be counted
        i_cell = i
        j_cell = j
        while ((not self._limit_left(i, j, i_cell, j_cell)) and
               (symbol in self.board[i_cell][j_cell])):
            score_left += 1
            j_cell -= 1

        score_right: int = -1
        i_cell = i
        j_cell = j
        while ((not self._limit_right(i, j, i_cell, j_cell)) and
               (symbol in self.board[i_cell][j_cell])):
            score_right += 1
            j_cell += 1

        score_horizontal: int = score_left + score_right + 1

        # -- Main diagonal, from top left to bottom right
        score_top_left = -1  # not 0 because current cell will be counted
        i_cell = i
        j_cell = j
        while ((not self._limit_top(i, j, i_cell, j_cell)) and
               (not self._limit_left(i, j, i_cell, j_cell)) and
               (symbol in self.board[i_cell][j_cell])):
            score_top_left += 1
            i_cell -= 1
            j_cell -= 1

        score_bottom_right: int = -1
        i_cell = i
        j_cell = j
        while ((not self._limit_bottom(i, j, i_cell, j_cell)) and
               (not self._limit_right(i, j, i_cell, j_cell)) and
               (symbol in self.board[i_cell][j_cell])):
            score_bottom_right += 1
            i_cell += 1
            j_cell += 1

        score_diagonal_main: int = score_top_left + score_bottom_right + 1

        # -- Secondary diagonal, from top right to botom left
        score_top_right: int = -1  # not 0 because current cell will be counted
        i_cell = i
        j_cell = j
        while ((not self._limit_top(i, j, i_cell, j_cell)) and
               (not self._limit_right(i, j, i_cell, j_cell)) and
               (symbol in self.board[i_cell][j_cell])):
            score_top_right += 1
            i_cell -= 1
            j_cell += 1

        score_bottom_left: int = -1
        i_cell = i
        j_cell = j
        while ((not self._limit_bottom(i, j, i_cell, j_cell)) and
               (not self._limit_left(i, j, i_cell, j_cell)) and
               (symbol in self.board[i_cell][j_cell])):
            score_bottom_left += 1
            i_cell += 1
            j_cell -= 1

        score_diagonal_secondary: int = score_top_right + score_bottom_left + 1

        scores: dict = {
            "Vertical": score_vertical,
            "Horizontal": score_horizontal,
            "Diagonal Main": score_diagonal_main,
            "Diagonal Secondary": score_diagonal_secondary
        }

        '''
        # this may help other player to pay attention, which is not ideal...
        print("Last move score", scores)
        '''

        # See if board is solved
        for score in scores.values():
            if self.line_length <= score:
                self.solved = True

        return True

    def is_solved(self) -> bool:
        """Get the state of the board.

        Args:
            None

        Returns:
            True when the board is solved.

        Raises:
            None
        """
        return self.solved

    def get_player_moves(self) -> list[int]:
        """Get the list of player IDs on order of moves.

        Args:
            None

        Returns:
            player_moves: list[int] of player IDs in the order of moves

        Raises:
            None
        """
        return self.player_moves

    def _put(self, column: int, i_symbol: int) -> bool:
        """Place a stone on a board.

        Args:
            column: int index of column where to put the stone.
            i_sumbol: int index of stone(color) symbol to place.

        Returns:
            True when stone is placed, false if column if full.

        Raises:
            None
        """
        if self.columns_height[column] == self.height:
            print("Column", column, "is full, better luck next time!")
            return False
        else:
            i_stone = self.height - self.columns_height[column] - 1
            self.board[i_stone][column] = self.SYMBOLS[i_symbol]
            self.columns_height[column] += 1
            self.empty_cells_left -= 1
            return True

    def apply(self, column: int, player_id: int, player_name: str) -> bool:
        """Apply the proposed player's move to the board.

        Args:
            column: int index of column where to put the stone.
            player_id: int index of stone(color) symbol to use.
            player_name: string to display user name if them won.

        Returns:
            True when move performed

        Raises:
            ValueError: If column is not in range from 0 to board.width-1.
            ValueError: If player ID negative or greater than the number
                        of available stones.
        """

        if column < 0 or self.width <= column:
            raise ValueError(
                "Column index has to be from 0 to Board.width-1" +
                " which is", self.width-1,
                ", and not", column
            )

        if player_id < 0 or self.N_SYMBOLS <= player_id:
            raise ValueError(
                "Player ID, an index, sould be positive integer" +
                "from 0 to board.n_SYMBOLS-1 (max number of players1-1)" +
                ", which is", self.N_SYMBOLS-1,
                ", and not", player_id
            )

        # Place the stone
        if not self._put(column, player_id):
            return False
        else:
            self.player_moves.append(player_id)

        is_playable = self._check(column)

        if self.is_solved():
            print(player_name + " Won!")
        else:
            if not is_playable:
                self.solved = True
                print("\n\nDraw :CСС\n\n")
                return False
            else:
                # keep playing
                pass

        return True
