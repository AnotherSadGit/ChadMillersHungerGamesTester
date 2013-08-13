from __future__ import division, print_function
from argparse import ArgumentParser

from app import DEFAULT_VERBOSITY, DEFAULT_MIN_ROUNDS, \
    DEFAULT_AVERAGE_ROUNDS, DEFAULT_END_EARLY, DEFAULT_PLAYERS, \
    DEFAULT_LOG_FILE
from bots import *
from Player import Player


def get_arguments():
    '''
    get_arguments()

    Read the bot and Game arguments from the command arguments.

    For help, run `python app.py -h` or `python app.py --help`
    '''
    parser = ArgumentParser()

    bot_options = parser.add_argument_group("bots to use for game")    
    bot_options.add_argument("-p", "--pushover", dest="pushover",
                        default=0, type=int,
                        help="the number of Pushover bots to play with")
    bot_options.add_argument("-f", "--freeloader", dest="freeloader",
                        default=0, type=int,
                        help="the number of Freeloader bots to play with")
    bot_options.add_argument("-a", "--alternator", dest="alternator",
                        default=0, type=int,
                        help="the number of Alternator bots to play with")
    bot_options.add_argument("-m", "--max-rep-hunter", dest="mrp",
                        default=0, type=int,
                        help="the number of MaxRepHunter bots to play with")
    bot_options.add_argument("-fh", "--fair-hunter", dest="fairhunter",
                        default=0, type=int,
                        help="the number of FairHunter bots to play with")
    bot_options.add_argument("-ah", "--avg-hunter", dest="averagehunter",
                        default=0, type=int,
                        help="the number of AverageHunter bots to play with")
    bot_options.add_argument("-pl", "--player", dest="player",
                        default=0, type=int,
                        help="number of Player bots as defined in Player.py")
    bot_options.add_argument("-r", "--random", dest="random",
                        default=[], nargs="*",
                        help="the number and value of Random bots to play " \
                        "with (in the form 'number,p_hunt' such that number " \
                        "is an int, and p_hunt is a float from 0-1)")
    bot_options.add_argument("-bh", "--bounded-hunter", dest="boundedhunter",
                        default=[], nargs="*",
                        help="the number and values of BoundedHunter bots to play " \
                        "with (in the form 'number,lower,upper' such that number " \
                        "is an int, and lower & upper are floats from 0-1)")
    bot_options.add_argument("-fth", "--fixed-threshold", dest="fixedthreshold",
                        default=[], nargs="*",
                        help="the number, threshold and first value of " \
                        "Fixed Threshold bots to play with (in the form " \
                        "'number,threshold,first_hunt_value' " \
                        "such that number is an int, threshold is a float from 0-1, " \
                        "and first_hunt_value is either 'h' or 's')")
    
    game_options= parser.add_argument_group("game options")
    game_options.add_argument("-q", "--quiet", dest="verbose",
                        default=not DEFAULT_VERBOSITY, action="store_false",
                        help="use quiet output (off by default)")
    game_options.add_argument("-l", "--min-rounds", dest="min_rounds",
                        default=DEFAULT_MIN_ROUNDS, type=int,
                        help="the minimum number of rounds to play")
    game_options.add_argument("-x", "--average-rounds", dest="average_rounds",
                        default=DEFAULT_AVERAGE_ROUNDS, type=int,
                        help="the average number of rounds to play")
    game_options.add_argument("-e", "--end-early", dest="end_early",
                        default=DEFAULT_END_EARLY, action="store_true",
                        help="end the game if 'Player' is eliminated")
    game_options.add_argument("-lf", "--log-filename", dest="log_filename",
                        default=DEFAULT_LOG_FILE, 
                        help="name of output file")
    
    args = parser.parse_args()

    options = {
        "verbose": not args.verbose,
        "min_rounds": args.min_rounds,
        "average_rounds": args.average_rounds,
        "end_early": args.end_early,
        "log_filename": args.log_filename
    }

    bots = []    
    bots.extend(
        [Pushover() for _ in range(args.pushover)] +
        [Freeloader() for _ in range(args.freeloader)] +
        [Alternator() for _ in range(args.alternator)] +
        [MaxRepHunter() for _ in range(args.mrp)] +
        [FairHunter() for _ in range(args.fairhunter)] +
        [AverageHunter() for _ in range(args.averagehunter)] +
        [Player() for _ in range(args.player)]
        )        

    for r in args.random:
        (num, value) = r.split(",")
        num = int(num)
        value = float(value)
        
        bots.extend([Random(value) for _ in range(num)])              

    for r in args.boundedhunter:
        (num, lower, upper) = r.split(",")
        num = int(num)
        lower = float(lower)
        upper = float(upper)
        
        bots.extend([BoundedHunter(lower, upper) for _ in range(num)]) 

    for r in args.fixedthreshold:
        (number, threshold, first_hunt_value) = r.split(",")
        number = int(number)
        threshold = float(threshold)
        
        bots.extend([FixedThreshold(threshold, first_hunt_value) 
                     for _ in range(number)])

    players = bots if bots else DEFAULT_PLAYERS       
        
    return (players, options)

