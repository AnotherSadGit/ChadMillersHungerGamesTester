from __future__ import division, print_function

from datetime import datetime

import arguments
from Game import Game
from bots import *
from Player import Player
from ThresholdPlayers import FixedThreshold


# Change these to edit the default Game parameters
DEFAULT_VERBOSITY = True
DEFAULT_MIN_ROUNDS = 300
DEFAULT_AVERAGE_ROUNDS = 1000
DEFAULT_END_EARLY = False
# Set log file to None to divert output to stdout.
DEFAULT_LOG_FILE = "game_{0:%Y%m%d_%H%M%S}.txt".format(datetime.now())
DEFAULT_PLAYERS = [Player(), Pushover(), Freeloader(), Alternator(), 
                   MaxRepHunter(), FairHunter(), AverageHunter(), 
                   Random(.2), Random(.8), BoundedHunter(0.7, 1.0), 
                   FixedThreshold(0.5, 'h', True), FixedThreshold(0.5, 's'), 
                   FixedThreshold(0.45, 'h'), FixedThreshold(0.45, 's'), 
                   FixedThreshold(0.55, 'h', True), FixedThreshold(0.55, 's')]

# Bare minimum test game. See README.md for details.

if __name__ == '__main__':
    (players, options) = arguments.get_arguments()
    # The list of players for the game is made up of
    #   'Player' (your strategy)
    #   bots from get_arguments (the bots to use)
    player_list = players
    # **options -> interpret game options from get_arguments
    #              as a dictionary to unpack into the Game parameters
    game = Game(player_list, **options)
    game.play_game()
