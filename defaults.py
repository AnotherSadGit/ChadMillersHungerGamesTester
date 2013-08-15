'''Separate the default data from the application code.'''

from __future__ import division, print_function

from datetime import datetime

from bots import *
from Player import Player

# Change these to edit the default Game parameters
DEFAULT_VERBOSITY = True
DEFAULT_MIN_ROUNDS = 300
DEFAULT_AVERAGE_ROUNDS = 1000
DEFAULT_END_EARLY = False
# Set log file to None to divert output to stdout.
DEFAULT_LOG_FILE = "game_{0:%Y%m%d_%H%M%S}.txt".format(datetime.now())
DEFAULT_PLAYERS = [Player(), Pushover(), Freeloader(), Alternator(), 
                   MaxRepHunter(), FairHunter(), AverageHunter(), 
                   Random(.2), Random(.8), BoundedHunter(0.7, 1.0)]