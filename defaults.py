'''Separate the default data from the application code.'''

from __future__ import division, print_function

from bots import *
from Player import Player
from ThresholdPlayers import FixedThreshold

# Change these to edit the default Game parameters
DEFAULT_VERBOSITY = True
DEFAULT_MIN_ROUNDS = 300
DEFAULT_AVERAGE_ROUNDS = 1000
DEFAULT_END_EARLY = False
# Set log file to None to divert output to stdout.
DEFAULT_LOG_FILE = "game.txt"
DEFAULT_PLAYERS = [Player(), Pushover(), Freeloader(), Alternator(), 
                   MaxRepHunter(), FairHunter(), AverageHunter(), 
                   Random(.2), Random(.8), BoundedHunter(0.7, 1.0), 
                   FixedThreshold(0.5, 'h'), FixedThreshold(0.5, 's'), 
                   FixedThreshold(0.45, 'h'), FixedThreshold(0.45, 's'), 
                   FixedThreshold(0.55, 'h'), FixedThreshold(0.55, 's')]