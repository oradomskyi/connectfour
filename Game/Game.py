from typing import Optional

from time import sleep
from threading import Thread, Lock
from random import randint

from warnings import warn

from .Board.Board import Board
from .Player.Player import Player
from .Player.PlayerHuman import PlayerHuman

HELP_TEXT = """Please initialize Game with the dictinary, here is an example:

# I believe these variables are self-explanatory
board_width = 7
board_height = 6
board_line_length = 4

# Create a list with two "human" players and set their names
board_players = [ PlayerHuman(name="Fede"), PlayerHuman(name="Ale") ]

# add some more "computer" players - algo that makes random moves
#for i in range(0, 40):
#    board_players.append(PlayerAlgoRandom(n_moves=board_width))

# A dictionary describing the game settings
settings = {
    "players": board_players,
    "board": {
        "width": board_width,
        "height": board_height,
        "line_length": board_line_length
    },
    # when True players move one after the other in order of
    # the settings["players"] list
    # when False each player run in a separate Thread and is trying
    # to acquire Lock() after a random delay of a few seconds
    "boring": True
}
"""


class Game:
    """
    https://en.wikipedia.org/wiki/Connect_Four

    "Connect Four" is a game in which the players choose a color
    and then take turns dropping colored tokens into a six-row,
    seven-column vertically suspended grid. The pieces fall straight down,
    occupying the lowest available space within the column.
    The objective of the game is to be the first to form a horizontal,
    vertical, or diagonal line of four of one's own tokens.

    Class implement "facade" to the system and implements synchronous
    and asynchronous ways to play.
    (read more in the comments of play() function)

    In fact, current implementation allows for M,n,k Game with
    restriction on number of player to be not more than 42
    https://en.wikipedia.org/wiki/M,n,k-game
    """

    def __init__(self, settings: Optional[dict] = None):
        """Constructor
        prepares the list of symbols(colors) that could be used for
        different players by default there could be up to 42 players.
        Also initializes the board matrix, column height counter
        and other internal variables.

        Args:
            settings: A dictionary containing the setup.

            Example:

            settings = {
                "players": [PlayerHuman(name="Fede"), PlayerHuman(name="Ale")]
                , "board": {
                      "width" : 7
                    , "height" : 6
                    , "line_length" : 4
                }
                , "boring" : False
            }

        Returns:
            None

        Raises:
            AttributeError: If settings has no entry "board".
            AttributeError: If settings["board"] has no entry "width".
            AttributeError: If settings["board"] has no entry "height".
            AttributeError: If settings["board"] has no entry "line_length".
            AttributeError: If settings has no entry "players".
            TypeError: If settings is None.
            TypeError: If settings["players"] value is not a list [].
            TypeError: If settings["players"] items are not subclass of Player.
        """

        if settings is None:
            # we got no setting from the user :CCC
            print(HELP_TEXT)
            raise TypeError("settings should be dictionary, and not", settings)

        # The Board could could be instantiated only in case
        # all given parameters are correct
        # We will not test if width, height and line_length
        # are of type int as this would clutter the code even more...

        if "board" not in settings:
            print(HELP_TEXT)
            raise AttributeError(
                ('Properties of a game Board are ' +
                 'not specified in the settings dict:'),
                settings)

        if "width" not in settings["board"]:
            raise AttributeError(
                ('Width of a game Board is not ' +
                 'specified in the settings dict:'),
                settings)

        if "height" not in settings["board"]:
            raise AttributeError(
                ('Height of a game Board is not ' +
                 'specified in the settings dict:'),
                settings)

        if "line_length" not in settings["board"]:
            raise AttributeError(
                ('Line length of a game Board is not ' +
                 'specified in the settings dict:'),
                settings)

        # at this point things seem to be somewhat correct to try
        # instantiation of the Board class
        self.board: Board = Board(
            settings["board"]["width"],
            settings["board"]["height"],
            settings["board"]["line_length"]
        )

        # Check if Player list is provided and instances
        # are correctly initialized, if yes - add them to
        # internal list for later use
        if "players" not in settings:
            print(HELP_TEXT)
            raise AttributeError(
                'List of players is not specified in the settings dict:',
                settings)

        self.players: Optional[list[Player]] = None

        if not isinstance(settings["players"], list):
            raise TypeError(
                ("settings['players'] should be " +
                 "a list [], and not"),
                type(settings["players"]))

        for player in settings["players"]:
            if not issubclass(type(player), Player):
                raise TypeError(
                    ("Players has to of type Player, " +
                     "but you gave me"),
                    type(player))

            # Will init an empty list
            # in case if anything wrong with player type list will stay None
            # as I do not want to allocate it and cause errors later passing
            # aroung allocated but uninitialized variable
            if self.players is None:
                self.players = []

            # Pick a symbol(color) for each player
            player.set_ID(self.board.next_unused_stone())

            self.players.append(player)

        # Set a flag if game is single-threaded or multi-threaded
        self.boring: bool = True
        if "boring" in settings:
            self.boring = settings["boring"]

    def play(self):
        """Implements dynamics if the Connect Four game.

        Either single-thread syncronous play or multi-threaded asynchronous
        play, the decision is made based on internal boolean variable
            Game.boring.

        When Game.boring is True
            The Game enters the while loop until the board is solved or
            no moves left, and letting players to move in the exact order
            they are placed in the Game.players list

        When Game.boring is False
            Each player run their own thread with while loop until the board
            is solved or no moves left. In this case players compete for the
            board resource and are trying to acquire() the Lock object so no
            two players read or write the contents of the board simultaneously.
            Before each attempt player has to wait for a random amount of time,
            from zero up to several seconds. This gives a chance that a player
            would be given(or not given) several consecutive moves in a row.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        if self.boring is True:
            msg = ("\n\nMeh.. Ok, let's play a boring, "
                   "orthodox and synchronous way :)\n\n")

            warn(msg)

            print(self.board)

            can_play = True
            while can_play:
                for player in self.players:
                    if self.board.is_solved():
                        can_play = False
                        # exit the for loop
                        break

                    # game is not finished yet and this Player can play
                    print(player, self.board.get_symbol(player.get_ID()))
                    player.move(self.board)
                    print(self.board)

        else:
            msg = ("\n\nYa-pa-yeee! Async - this is " +
                   "where the real fun begins! XDDD\n\n")

            warn(msg)

            print(self.board)
            # We would need more advanced player.move() function
            # that would be independent of outer while loop that
            # is checking on board.is_solved(),
            # and to have this while routine inside the new move() function
            # so players are fundamentally independent of anything and
            # given only the board to play on
            #
            # Players are going to compete for taking an action on the Board,
            # and to ensure only one player at a time has acces to the board
            # we would need to clock others from taking control, this can be
            # done using what is called 'synchronization' mechanism
            #
            # This Game here is designed in such a way that a bare minimum
            # synchronization with only a single Lock object is sufficient

            # Decorator for the player.move()
            def move_async(board: Board, player: Player, lock: Lock):
                """Put player.move() inside the while loop
                polling on lock.acquire()."""
                # Intoruce Luck and make board available to Players
                # by chance...
                max_delay_ms = 1000
                if isinstance(player, PlayerHuman):
                    max_delay_ms = 5000

                can_play = True
                while can_play:
                    # Generate random delay time in seconds
                    delay = randint(0, max_delay_ms)/1000

                    # wait before trying to acquire lock
                    sleep(delay)

                    if lock.acquire():
                        # Got lucky and acquired the Lock!
                        # So now Player can make a move :)

                        # check if game already won by somebody else
                        if board.is_solved():
                            can_play = False
                            lock.release()  # don't forget to release the lock!

                            # just continue to exit the while loop. We could
                            # directly return and jump away from function but
                            # that does not seem right as there could be other
                            # statements after the while loop
                            continue

                        # game is not finished yet and this Player can play
                        print(player, board.get_symbol(player.get_ID()))
                        player.move(board)
                        print(board)

                        lock.release()  # don't forget to release the lock!
                    else:
                        # keep polling on lock.acquire()
                        pass

                print("Player", player.get_name(), " exit")
                # here could be some more code to execute after
                # exiting the while loop, some other logic
                # or the cleanup procedures

            # Lock is the synchronization object to ensure no players
            # modify the Board simultaneously, as well as no players
            # can move after board is solved or no moves left
            #
            # We can keep this object in the local scope of this if-else,
            # as our decorator function has access to everything
            # in the current scope - we don't need to pass it
            # inside the function.
            #
            # but I feel this somewhat obscures usage of objects when
            # relying on user's understanding of scopes, so I will pass
            # lock explicitly as a parameter to make it clear what is being
            # used and where.
            #
            # And I have no problems with this lock object is mutable
            # and would be passed by reference, so all threads would use
            # the same object no matter what.
            lock = Lock()

            # Get the show on the road!
            for player in self.players:
                # create a dedicated Thread for a Player with entry
                # at move_async() function we created earlier
                # and pass there board, player, and lock objects
                t = Thread(
                    target=move_async,
                    kwargs={
                        'board': self.board,
                        'player': player,
                        'lock': lock
                    }
                )

                # Start the thread
                t.start()

                # we do not want to join() as it will cause blocking
                # on the main thread until this one finishes
                # and we do not need to setDaemon() because we do not
                # want, do not need, and do not care for any thread
                # to continue after game is done!
