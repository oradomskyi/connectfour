Connect Four

https://en.wikipedia.org/wiki/Connect_Four

A board game in which the players choose a color and then take turns dropping colored tokens into a six-row, seven-column vertically suspended grid. The pieces fall straight down, occupying the lowest available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own tokens.

The current implementation has been written and tested with Python 3.9.2 and does not require any of non-standard libraries.

It supports single-thread synchronous play and multi-threaded asynchronous play, the decision is made based on the internal boolean variable 'game.boring' that is during initialization.

        When Game.boring is True
            The Game enters the while loop until the board is solved or
            no moves left and letting players move in the exact order
            they are placed in the Game.players list

        When Game.boring is False
            Each player runs their thread with a while loop until the board
            is solved or no moves left. In this case, players compete for the
            board resource and are trying to acquire() the Lock object so no
            two players read or write the contents of the board simultaneously.
            Before each attempt player has to wait for a random amount of time,
            from zero up to several seconds. This gives a chance that a player
            would be given(or not given) several consecutive moves in a row.
            
The current implementation allows for "M,n,k Game" with a restriction on the number of players to be not more than 42.

https://en.wikipedia.org/wiki/M,n,k-game

Known issues:
- Unit test coverage is incomplete, not all of the edge cases are tested.
- Runtime checks are incomplete, not all of the parameters are tested for correct values.
- Documentation is incomplete as it lacks flow and state diagrams.
- Stone symbols are not displayed correctly in Windows CMD.
- Spelling and typos in comments.
