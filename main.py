from Game.Game import Game
from Game.Player.PlayerHuman import PlayerHuman
from Game.Player.PlayerAlgoRandom import PlayerAlgoRandom

'''https://en.wikipedia.org/wiki/Connect_Four

    "Connect Four" is a game in which the players choose a color
    and then take turns dropping colored tokens into a six-row,
    seven-column vertically suspended grid. The pieces fall straight down,
    occupying the lowest available space within the column.
    The objective of the game is to be the first to form a horizontal,
    vertical, or diagonal line of four of one's own tokens.

    https://en.wikipedia.org/wiki/Connect_Four


In fact, current implementation allows for asynchronous M,n,k Game
with restriction on number of players to be not more than 42
https://en.wikipedia.org/wiki/M,n,k-game

For more info on async read the Game class docs
For more info on M,n,k read the Board class docs
'''

# I believe these variables are self-explanatory
board_width = 7
board_height = 6
board_line_length = 4

# Create a list with two "human" players and set their names
#
# From a design point of view, Players could be instantiated later,
# but that would severely limit ability to customize the instances
# without code duplication

# list of Player istances
board_players = [
    PlayerHuman(
        name="Fede",
        phrases=[' ', 'Well-well...', 'Ha!', 'Ough.']
    ),
    PlayerHuman(
        name="Ale",
        phrases=[
            ' ',
            'Weeee!',
            'A-ha-ha!',
            '*sneezing*',
            '*scratches the head*',
            '*crying in Korean*',
        ]
    )
]

# add some more "computer" players - algo that makes random moves
# for i in range(0, 40):
#     board_players.append(PlayerAlgoRandom(n_moves=board_width))

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
    # when False each player run in a separate Thread
    # and trying to acquire Lock() after a random delay
    # of the few seconds
    "boring": True
}

if __name__ == "__main__":
    # Begin the play only when this file is run from console,
    # othervise variables are loaded into runtime when file
    # is included as module or called from another script
    Game(settings).play()
