from __future__ import division, print_function
from argparse import ArgumentParser

from defaults import DEFAULT_VERBOSITY, DEFAULT_MIN_ROUNDS, \
    DEFAULT_AVERAGE_ROUNDS, DEFAULT_END_EARLY, DEFAULT_PLAYERS, \
    DEFAULT_LOG_FILE
from bots import *
from Player import Player
from ThresholdPlayers import FixedThreshold
from AntiSocialPlayers import RandomAntiSocial, FairHunterAntiSocial
from DetectivePlayers import RandomAntiSocialGTFT, RandomAntiSocialPavlov2

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
    parser = ArgumentParser(description="Tournament app for testing the " \
        "player classes created for the brilliant.org Hunger Games games " \
        "theory programming tournament.", 
                            epilog="Multiple bots of the same type can " \
                                "be created with different arguments by " \
                                "separating the argument groups with " \
                                "spaces. eg --random 3,0.5,0 2,0.8,0")

    game_options = parser.add_argument_group("game options")
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
    bot_options.add_argument("-fh", "--fair-hunter", dest="fairhunter",
                        default=[], nargs="*",
                        help="the number of FairHunter bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form 'number,do_log' " \
                            "where number is an int and do_log is 0 or 1")
    bot_options.add_argument("-ah", "--avg-hunter", dest="averagehunter",
                        default=[], nargs="*",
                        help="the number of AverageHunter bots to play " \
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
                        help="the number and probability of Random bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form  " \
                            "'number,p_hunt,do_log' where number is an int, " \
                            "p_hunt is a float in the range 0-1, and " \
                            "do_log is 0 or 1.")
    bot_options.add_argument("-bh", "--bounded-hunter", dest="boundedhunter",
                        default=[], nargs="*",
                        help="the number and limits of BoundedHunter bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form  " \
                            "'number,lower,upper,do_log' where number is an int, " \
                            "lower and upper are floats in the range 0-1, and " \
                            "do_log is 0 or 1")
    bot_options.add_argument("-fth", "--fixed-threshold", dest="fixedthreshold",
                        default=[], nargs="*",
                        help="the number, threshold and first value of " \
                            "FixedThreshold bots to play with, and whether " \
                            "they require detailed logging or not, in the form  " \
                            "'number,threshold,first_hunt_value,do_log' " \
                            "where number is an int, threshold is a float " \
                            "in the range 0-1, first_hunt_value is 'h' or 's' " \
                            "and do_log is 0 or 1")
    bot_options.add_argument("-ras", "--random-antisocial", dest="random_antisocial",
                        default=[], nargs="*",
                        help="the number and probabilities of RandomAntiSocial bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form  " \
                            "'number,p_hunt,antisocial_threshold,evil_threshold,do_log' " \
                            "where number is an int, " \
                            "p_hunt, antisocial_threshold and evil_threshold " \
                            "are floats in the range 0-1, " \
                            "and do_log is 0 or 1.")
    bot_options.add_argument("-fhas", "--fair-hunter-antisocial", dest="fairhunter_antisocial",
                        default=[], nargs="*",
                        help="the number and probabilities of " \
                            "FairHunterAntiSocial bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form  " \
                            "'number,antisocial_threshold,evil_threshold,do_log' " \
                            "where number is an int, " \
                            "antisocial_threshold and evil_threshold " \
                            "are floats in the range 0-1, " \
                            "and do_log is 0 or 1.")
    bot_options.add_argument("-rgt", "--random-antisocial-gtft", dest="random_antisocial_gtft",
                        default=[], nargs="*",
                        help="the number and probabilities of RandomAntiSocialGTFT bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form  " \
                            "'number,p_hunt,antisocial_threshold,evil_threshold,p_generosity,do_log' " \
                            "where number is an int, " \
                            "p_hunt, antisocial_threshold, evil_threshold " \
                            "and p_generosity are floats in the range 0-1, " \
                            "and do_log is 0 or 1.")
    bot_options.add_argument("-rpv", "--random-antisocial-pavlov", dest="random_antisocial_pavlov",
                        default=[], nargs="*",
                        help="the number and probabilities of RandomAntiSocialPavlov2 bots to play " \
                            "with, and whether they require detailed " \
                            "logging or not, in the form  " \
                            "'number,p_hunt,antisocial_threshold,evil_threshold,do_log' " \
                            "where number is an int, " \
                            "p_hunt, antisocial_threshold and evil_threshold " \
                            "are floats in the range 0-1, " \
                            "and do_log is 0 or 1.")
    
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
    add_player_group(bots, FairHunter, args.fairhunter) 
    add_player_group(bots, AverageHunter, args.averagehunter) 
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

    for x in args.boundedhunter:
        (number, lower, upper, do_log) = x.split(",")
        number = int(number)
        lower = float(lower)
        upper = float(upper)
        do_log = int(do_log)
        
        if number <= 0:
            continue
        elif number == 1:
            bots.append(BoundedHunter(lower, upper, None, do_log))
        else:
            bots.extend([BoundedHunter(lower, upper, i, do_log) for i in range(number)])

    for x in args.fixedthreshold:
        (number, threshold, first_hunt_value, do_log) = x.split(",")
        number = int(number)
        threshold = float(threshold)
        do_log = int(do_log)
        
        if number <= 0:
            continue
        elif number == 1:
            bots.append(FixedThreshold(threshold, first_hunt_value, None, do_log))
        else:
            bots.extend([FixedThreshold(threshold, first_hunt_value, i, do_log) for i in range(number)]) 

    for x in args.random_antisocial:
        (number, p_hunt, antisocial_threshold, evil_threshold, do_log) = x.split(",")
        number = int(number)
        p_hunt = float(p_hunt)
        antisocial_threshold = float(antisocial_threshold)
        evil_threshold = float(evil_threshold)
        do_log = int(do_log)
        
        if number <= 0:
            continue
        elif number == 1:
            bots.append(RandomAntiSocial(p_hunt, antisocial_threshold, 
                                         evil_threshold, None, do_log))
        else:
            bots.extend([RandomAntiSocial(p_hunt, antisocial_threshold, 
                                          evil_threshold, i, do_log) for i in range(number)])
                                          
    for x in args.fairhunter_antisocial:
        (number, antisocial_threshold, evil_threshold, do_log) = x.split(",")
        number = int(number)
        antisocial_threshold = float(antisocial_threshold)
        evil_threshold = float(evil_threshold)
        do_log = int(do_log)
        
        if number <= 0:
            continue
        elif number == 1:
            bots.append(FairHunterAntiSocial(antisocial_threshold, 
                                         evil_threshold, None, do_log))
        else:
            bots.extend([FairHunterAntiSocial(antisocial_threshold, 
                                          evil_threshold, i, do_log) for i in range(number)])

    for x in args.random_antisocial_gtft:
        (number, p_hunt, antisocial_threshold, evil_threshold, p_generosity, do_log) = x.split(",")
        number = int(number)
        p_hunt = float(p_hunt)
        antisocial_threshold = float(antisocial_threshold)
        evil_threshold = float(evil_threshold)
        p_generosity = float(p_generosity)
        do_log = int(do_log)
        
        if number <= 0:
            continue
        elif number == 1:
            bots.append(RandomAntiSocialGTFT(p_hunt, antisocial_threshold, 
                                         evil_threshold, p_generosity, 
                                         None, do_log))
        else:
            bots.extend([RandomAntiSocialGTFT(p_hunt, antisocial_threshold, 
                                          evil_threshold, p_generosity, 
                                          i, do_log) for i in range(number)])

    for x in args.random_antisocial_pavlov:
        (number, p_hunt, antisocial_threshold, evil_threshold, do_log) = x.split(",")
        number = int(number)
        p_hunt = float(p_hunt)
        antisocial_threshold = float(antisocial_threshold)
        evil_threshold = float(evil_threshold)
        do_log = int(do_log)
        
        if number <= 0:
            continue
        elif number == 1:
            bots.append(RandomAntiSocialPavlov2(p_hunt, antisocial_threshold, 
                                         evil_threshold, 
                                         None, do_log))
        else:
            bots.extend([RandomAntiSocialPavlov2(p_hunt, antisocial_threshold, 
                                          evil_threshold, 
                                          i, do_log) for i in range(number)])
        
    players = bots if bots else DEFAULT_PLAYERS       
        
    return (players, options)

