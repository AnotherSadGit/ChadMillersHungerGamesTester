from __future__ import division, print_function
from argparse import ArgumentParser

from defaults import DEFAULT_VERBOSITY, DEFAULT_MIN_ROUNDS, \
    DEFAULT_AVERAGE_ROUNDS, DEFAULT_END_EARLY, DEFAULT_PLAYERS, \
    DEFAULT_LOG_FILE
from bots import *
from Player import Player

def add_player_group(player_list, player_class, argument_values):
    for x in argument_values:
        (number, do_log) = x.split(",")
        number = int(number)
        do_log = int(do_log)
        
        if number <= 0:
            return
        elif number == 1:
            player_list.append(player_class(None, do_log))
        else:
            player_list.extend([player_class(i, do_log) for i in range(number)])

def get_arguments():
    '''
    get_arguments()

    Read the bot and Game arguments from the command arguments.

    For help, run `python app.py -h` or `python app.py --help`
    '''
    parser = ArgumentParser()

    bot_options = parser.add_argument_group("bots to use for game")    
    bot_options.add_argument("-p", "--pushover", dest="pushover",
                        default=[], nargs="*",
                        help="the number of Pushover bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form 'number,do_log' " \
                            "where number is an int and do_log is 0 or 1")
    bot_options.add_argument("-f", "--freeloader", dest="freeloader",
                        default=[], nargs="*",
                        help="the number of Freeloader bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form 'number,do_log' " \
                            "where number is an int and do_log is 0 or 1")
    bot_options.add_argument("-a", "--alternator", dest="alternator",
                        default=[], nargs="*",
                        help="the number of Alternator bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form 'number,do_log' " \
                            "where number is an int and do_log is 0 or 1")
    bot_options.add_argument("-m", "--max-rep-hunter", dest="mrp",
                        default=[], nargs="*",
                        help="the number of MaxRepHunter bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form 'number,do_log' " \
                            "where number is an int and do_log is 0 or 1")
    bot_options.add_argument("-pl", "--player", dest="player",
                        default=[], nargs="*",
                        help="the number of Player bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form 'number,do_log' " \
                            "where number is an int and do_log is 0 or 1")
    bot_options.add_argument("-r", "--random", dest="random",
                        default=[], nargs="*",
                        help="the number and value of Random bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form  " \
                            "'number,p_hunt,do_log' where number is an int, " \
                            "p_hunt is a float in the range 0-1, and " \
                            "do_log is 0 or 1")

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
    
    add_player_group(bots, Pushover, args.pushover) 
    add_player_group(bots, Freeloader, args.freeloader) 
    add_player_group(bots, Alternator, args.alternator) 
    add_player_group(bots, MaxRepHunter, args.mrp) 
    add_player_group(bots, Player, args.player) 

    for x in args.random:
        (number, p_hunt, do_log) = x.split(",")
        number = int(number)
        p_hunt = float(p_hunt)
        do_log = int(do_log)
        
        if number <= 0:
            continue
        elif number == 1:
            bots.append(Random(p_hunt, None, do_log))
        else:
            bots.extend([Random(p_hunt, i, do_log) for i in range(number)])
        
    players = bots if bots else DEFAULT_PLAYERS       
        
    return (players, options)

