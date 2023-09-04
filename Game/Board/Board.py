from random import choice, randint
from warnings import warn


class Board:
    """The logic of the "Connect Four" game, and produces output to the console. 
    """

    def __init__(self, width: int, height: int, line_length: int):
        """Prepares the list of symbols(colors) that could be used for players.

        By default there could be up to 42 players. Initializes the board
        matrix, column height counter and other internal variables.

        Args:
            width: width of the gaming board, expected to be positive integer greater than zero
            height: A port value greater or equal to 1024.
            line_length: A port value greater or equal to 1024.

        Returns:
            None

        Raises:
            !!!!!!!!!!!!!!!!!!!!!!!!!ConnectionError: If no available port is found.
        """

        # https://en.wikipedia.org/wiki/Geometric_Shapes_(Unicode_block)
        self.n_symbols = 42
        self.symbols_start = ord("\u25b0")
        self.symbols = [ chr(self.symbols_start + i) for i in range(0, self.n_symbols) ]
        
        print("\n\nBoard says:\nI have", self.n_symbols,"symbols:", self.symbols)
        
        self.i_symbol = 0
        self.empty_symbol = ' '
        self.solved = False
        self.empty_cells_left = width*height

        # Let's dive into initializaton...
        if 0 < width:
            self.width = width
        else:
            raise ValueError("I am not sure how play on a Board of width", width)

        if 0 < height:
            self.height = height
        else:
            raise ValueError("I am not sure how play on a Board of height", height)

        if 0 < line_length:
            if line_length <= self.width and line_length <= self.height:
                self.line_length = line_length
            else:
                raise ValueError("Line is toooo long, it sould be no bigget than board width which is", self.width,", and not", line_length)
        
        # Create a matrix for storing state of the game
        self.board = [[self.empty_symbol for i in range(0, self.width)] for j in range(0, self.height)]

        # Create indexing for the columns
        self.columns_height = [0 for i in range(0, self.width)]
        
    def __str__(self) -> str:
        """Constructor
        prepares the list of symbols(colors) that could be used for different players
        by default there could be up to 42 players. Also initializes the board matrix,
        column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """

        text = "\n\n"
        
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

    def next_player_id(self) -> int:
        """Constructor
        prepares the list of symbols(colors) that could be used for different players
        by default there could be up to 42 players. Also initializes the board matrix,
        column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """

        if self.i_symbol == self.n_symbols:
            raise Exception("Board says: Wow-wow, I do not have capacity for more than",self.n_symbols,"players!")

        self.i_symbol += 1
        return self.i_symbol-1

    def get_symbol(self, i_symbol: int) -> str:
        """Constructor
        prepares the list of symbols(colors) that could be used for different players
        by default there could be up to 42 players. Also initializes the board matrix,
        column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """
        
        if i_symbol < 0 or self.n_symbols <= i_symbol:
            raise ValueError("Player ID, an index, sould be positive integer from 0 to board.n_symbols-1 (max number of players1-1), which is",self.n_symbols-1,", and not", i_symbol)

        return self.symbols[i_symbol]

    def get_width(self) -> int:
        """Constructor
        prepares the list of symbols(colors) that could be used for different players
        by default there could be up to 42 players. Also initializes the board matrix,
        column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """
        return self.width
    
    def _limit_top(self, i: int, j: int, idx: int, jdx: int) -> bool:
        """Constructor
        prepares the list of symbols(colors) that could be used for different players
        by default there could be up to 42 players. Also initializes the board matrix,
        column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """
        return (idx < 0) or (idx < i-self.line_length)

    def _limit_bottom(self, i: int, j: int, idx: int, jdx: int) -> bool:
        """Constructor
        prepares the list of symbols(colors) that could be used for different players
        by default there could be up to 42 players. Also initializes the board matrix,
        column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """
        return (self.height <= idx) or (i+self.line_length < idx)

    def _limit_left(self, i: int, j: int, idx: int, jdx: int) -> bool:
        """Constructor
        prepares the list of symbols(colors) that could be used for different players
        by default there could be up to 42 players. Also initializes the board matrix,
        column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """
        return (jdx < 0) or (jdx < j-self.line_length)

    def _limit_right(self, i: int, j: int, idx: int, jdx: int) -> bool:
        """Constructor
        prepares the list of symbols(colors) that could be used for different players
        by default there could be up to 42 players. Also initializes the board matrix,
        column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """
        return (self.width <= jdx) or (j+self.line_length < jdx)

    def _check(self, column: int) -> bool:
        """Constructor
        prepares the list of symbols(colors) that could be used for different players
        by default there could be up to 42 players. Also initializes the board matrix,
        column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """
        
        #print(self.empty_cells_left)
        if self.empty_cells_left == 0:
            return False

        # I do not know if there is any efficient way to test the board,
        # maybe it is not that bad to spawn recursion from the last move
        # in order not to re-compute entire board all over again..
        # but still - multiple cells would be evalated multiple times.

        # Get the last move location and symbol
        i = self.height - self.columns_height[column]
        j = column
        symbol = self.board[i][j]

        '''        
        # this may help other player to pay attention, which is not ideal...
        print("Last Move:", i, j, symbol)
        '''

        # We will test vertical, horizontal and two diagonals passing throught the 
        # cell of the last move for existense of a continuous line of at least self.line_length

        # -- Check cells Up and Down from current if there is a continuous line 
        # in the range i={-L, -L+1, .., 0, .., L-1, L} where L=line_length

        # Actually, situation when there are values in the column above the last move
        # is not possible, so I leave it here for my reference
        '''
        score_up = -1 # not 0 because current cell will be counted 
        idx = i
        jdx = j
        while (not self._limit_top(i, j, idx, jdx)) and (symbol in self.board[idx][jdx]):
            score_up += 1
            idx -= 1
        '''
        score_up = 0
        
        score_down = -1
        idx = i
        jdx = j
        while (not self._limit_bottom(i, j, idx, jdx)) and (symbol in self.board[idx][jdx]):
            score_down += 1
            idx += 1
        
        score_vertical = score_up + score_down + 1
        
        # -- Now let's do the same horizontaly
        score_left = -1 # not 0 because current cell will be counted 
        idx = i
        jdx = j
        while (not self._limit_left(i, j, idx, jdx)) and (symbol in self.board[idx][jdx]):
            score_left += 1
            jdx -= 1

        score_right = -1
        idx = i
        jdx = j
        while (not self._limit_right(i, j, idx, jdx)) and (symbol in self.board[idx][jdx]):
            score_right += 1
            jdx += 1
        
        score_horizontal = score_left + score_right + 1
        
        # -- Main diagonal, from top left to bottom right
        score_top_left = -1 # not 0 because current cell will be counted 
        idx = i
        jdx = j
        while (not self._limit_top(i, j, idx, jdx)) and \
              (not self._limit_left(i, j, idx, jdx)) and \
              (symbol in self.board[idx][jdx]):
            score_top_left += 1
            idx -= 1
            jdx -= 1
        
        score_bottom_right = -1
        idx = i
        jdx = j
        while (not self._limit_bottom(i, j, idx, jdx)) and \
              (not self._limit_right(i, j, idx, jdx)) and \
              (symbol in self.board[idx][jdx]):
            score_bottom_right += 1
            idx += 1
            jdx += 1

        score_diagonal_main = score_top_left + score_bottom_right + 1
        
        # -- Secondary diagonal, from top right to botom left
        score_top_right = -1 # not 0 because current cell will be counted 
        idx = i
        jdx = j
        while (not self._limit_top(i, j, idx, jdx)) and \
              (not self._limit_right(i, j, idx, jdx)) and \
              (symbol in self.board[idx][jdx]):
            score_top_right += 1
            idx -= 1
            jdx += 1
        
        score_bottom_left = -1
        idx = i
        jdx = j
        while (not self._limit_bottom(i, j, idx, jdx)) and \
              (not self._limit_left(i, j, idx, jdx)) and \
              (symbol in self.board[idx][jdx]):
            score_bottom_left += 1
            idx += 1
            jdx -= 1

        score_diagonal_secondary = score_top_right + score_bottom_left + 1
    
        scores = {
              "Vertical": score_vertical
            , "Horizontal": score_horizontal
            , "Diagonal Main": score_diagonal_main
            , "Diagonal Secondary": score_diagonal_secondary 
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
        """Constructor
        prepares the list of symbols(colors) that could be used for different players
        by default there could be up to 42 players. Also initializes the board matrix,
        column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """
        return self.solved

    def _put(self, column: int, i_symbol: int) -> bool:
        """Constructor
        prepares the list of symbols(colors) that could be used for different players
        by default there could be up to 42 players. Also initializes the board matrix,
        column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """
        if self.columns_height[column] == self.height:
            print("Column", column, "is full, better luck next time!")
            return False
        else:
            self.board[self.height - self.columns_height[column] - 1][column] = self.symbols[i_symbol]
            self.columns_height[column] += 1
            self.empty_cells_left -= 1
            return True

    def apply(self, column: int, player_id: int, player_name: str) -> bool:
        """Constructor
        prepares the list of symbols(colors) that could be used for different players
        by default there could be up to 42 players. Also initializes the board matrix,
        column height counter and other internal variables.

        Args:
            minimum: A port value greater or equal to 1024.

        Returns:
            The new minimum port.

        Raises:
            ConnectionError: If no available port is found.
        """

        if column < 0 or self.width <= column:
            raise ValueError("Column index has to be from 0 to Board.width-1, which is",self.width-1,", and not", column)
        
        if player_id < 0 or self.n_symbols <= player_id:
            raise ValueError("Player ID, an index, sould be positive integer from 0 to board.n_symbols-1 (max number of players1-1), which is",self.n_symbols-1,", and not", player_id)
        
        # Mark the board
        if not self._put(column, player_id):
            return False
        else:
            # we can continue and check if player won the game
            pass

        is_playable = self._check(column)

        #print("is_playable", is_playable, "self.is_solved()", self.is_solved())
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