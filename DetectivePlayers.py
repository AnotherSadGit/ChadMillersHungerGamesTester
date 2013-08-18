from Player import BasePlayer
import copy
import random

class BaseDetective(BasePlayer):
    '''Hunter in the Brilliant.org Hunger Games which attempts to identify 
    other players with unique reputations so it can track how they play 
    through multiple rounds of the tournament, despite the order of the other 
    players being shuffled between rounds.
    '''    

    # To attempt to identify the other player:
    # 1) At the start of a round record the other players' reputations;
    # 2) Forecast the worst case and best case reputations each player could 
    #       have at the end of the round.  Worst case = slack for all contests 
    #       in the round, best case = hunt for all contests in the round.
    # 3) At the start of the next round check how many players fall into the 
    #       forecast range (worst to best) for each reputation calculated in 
    #       the last round.  If only one player falls into the forecast range, 
    #       that player must be the same player from the previous round.

    # Identifying the player by itself is not enough.  Their choice (hunt or 
    # slack) from the previous round must be determined.  To do that, at the 
    # end of the previous round, when the results of the round are released, 
    # work out the other players' choices from the round results and 
    # record them with the forecast reputation ranges.  If a player is matched 
    # to a forecast reputation range their previous round's choice is then 
    # available.

    def __init__(self, name, single_hunt_function, id = None, do_logging = False):
        self.name = name
        super(BaseDetective, self).__init__(self.name, id, do_logging)

        # Function that returns either 'h' or 's', with the following signature:
        # single_hunt_function(round_number, current_food, current_reputation,
        #                      m, rep, player_history), 
        # where player_history is a dictionary with details of how the player 
        # played last round.  If the player's history hasn't been tracked the 
        # dictionary will be empty.
        self._single_hunt_function = single_hunt_function

        self._other_players = []
        self._unknown_players_details = []
        self._total_number_contests_per_player = 0


    def get_number_contests_this_round(self, players_reputations):
        number_players_this_round = len(players_reputations) + 1
        # Each player plays against each one of the other players, so each 
        # player has (number_players_this_round - 1) contests.
        return number_players_this_round * (number_players_this_round - 1)
    

    def forecast_player_reputation(self, player_reputation_end_last_round,
                                    total_contests_per_player_end_last_round,
                                    number_players_this_round):
        # By definition:
        # reputation = (total times a player has hunted already / 
        #               total number of contests player has already taken part in)

        # So:
        # total times a player has hunted already =
        #   (reputation * total number of contests player has already taken part in)
         
        # During the round each player will take part in 
        # (number_players_this_round - 1) contests.  That means in this round 
        # a player can hunt between 0 and (number_players_this_round - 1) times.
        
        # Lower bound for forecast reputation:
        # (total times a player has hunted already + 0) /
        # total number of contests player will have taken part in by end of this round

        # Upper bound for forecast reputation:
        # (total times a player has hunted already + (number_players_this_round - 1)) /
        # total number of contests player will have taken part in by end of this round

        # Where:
        # total number of contests player will have taken part in by end of this round = 
        # (total number of contests player has already taken part in + 
        #   (number_players_this_round - 1))
        
        player_total_hunts_end_last_round = (player_reputation_end_last_round *
                                             total_contests_per_player_end_last_round)
        total_contests_per_player_end_this_round = (total_contests_per_player_end_last_round +
                                                    (number_players_this_round - 1))
        forecast_low = 0
        forecast_high = 1
        if player_reputation_end_last_round <> 0:
            forecast_low = (player_total_hunts_end_last_round /
                            total_contests_per_player_end_this_round)
            forecast_high = ((player_total_hunts_end_last_round + (number_players_this_round - 1)) /
                             total_contests_per_player_end_this_round)
        player_reputation_forecast = (forecast_low, forecast_high)
        return player_reputation_forecast


    def forecast_players_reputations(self, players_reputations_end_last_round,
                                     total_contests_per_player_end_last_round, 
                                     players_uids = None):
        # The number of elements in players_reputations is 
        # (number_players_this_round - 1), as it does not include the 
        # reputation of the player represented by this class. 
        number_players_this_round = len(players_reputations_end_last_round) + 1
        if players_uids is None:
            unknown_players_details = \
                [{"prev_rep": rep, 
                  "rep_forecasts": self.forecast_player_reputation(rep, 
                                                              total_contests_per_player_end_last_round, 
                                                              number_players_this_round)
                              } for rep in players_reputations_end_last_round]
        else:
            players_details = zip(players_reputations_end_last_round, players_uids)
            unknown_players_details = \
                [{"prev_rep": rep, 
                  "player_name":player_name,
                  "rep_forecasts": self.forecast_player_reputation(rep, 
                                                              total_contests_per_player_end_last_round, 
                                                              number_players_this_round)
                              } for rep, player_name in players_details]

        return unknown_players_details
    

    def identify_players(self, actual_reputations_end_last_round, unknown_players_details):
        # It's possible to have two overlapping forecast reputation ranges, 
        # which have two actual player reputations in them.  Imagine the 
        # scenario where one of the overlapping forecast reputation ranges 
        # contains both actual reputations while the other forecast range 
        # contains only one of the actual reputations.  
        # eg
        # forecast rep range A: L-------------------U
        # forecast rep range B:              L----------------------U
        # actual rep x:                         x
        # actual rep y:                                     y
        # You can see that forecast range A contains only actual rep x, while  
        # forecast range B contains both actual reps x and y.

        # Doing a simple comparison we could find a match between forecast 
        # range A and actual rep x, since x is the only rep in the range.
        # However, we couldn't find a match for B, since it contains two 
        # actual reps, x and y.
        
        # We could find a match between B and y, however, if we eliminated x, 
        # since we've already found a match for it, and then tried again.  With 
        # x gone there is now only one actual rep, y, in range B so now we can 
        # find a match between B and y.
       
        # So once a match has been found, remove the matched actual rep and 
        # try again to find matches.  Repeat the match process as long as at 
        # least one match is found in the previous pass through the loop.

        # Want to ensure this is a list, not a tuple, so we can remove elements.
        players_reps = [rep for rep in actual_reputations_end_last_round]
        players_details = [[rep, {}] for rep in actual_reputations_end_last_round]
        match_found = True
        while match_found:
            match_found = False
            for player in unknown_players_details:
                matching_reputations = [rep for rep in players_reps
                                        if rep >= player["rep_forecasts"][0]
                                        and rep <= player["rep_forecasts"][1]]
                if len(matching_reputations) == 1:
                    match_found = True
                    matching_index = actual_reputations_end_last_round.index(matching_reputations[0])  
                    players_details[matching_index][1] = player
                    players_reps.remove(matching_reputations[0])
        return players_details


    def hunt_choices(self, round_number, current_food, current_reputation, m,
            player_reputations, players_uids = None):
        # WARNING: players_uids is non-standard parameter (parameters should 
        # conform to the interface spec in the rules).  It is supplied to allow 
        # for testing of the identify_players algorithm, to ensure it is 
        # identifying the players correctly.  The uid will be a combination of 
        # the player's name and an optional player's id.  The id will only be 
        # used if there are more than one player of the same type.
        players_details =  self.identify_players(player_reputations, self._unknown_players_details)
        if players_uids is not None:
            for i in range(len(players_details)):
                players_details[i][1]["uid"] = players_uids[i]
        # Record the player details to be used to identify players in the next round.
        self._unknown_players_details = \
            self.forecast_players_reputations(player_reputations, 
                                              self._total_number_contests_per_player, 
                                              players_uids)

        # Play the contests.
        hunt_results = [self._single_hunt_function(round_number,
                                                       current_food,
                                                       current_reputation,
                                                       m, rep, player_history)
                            for (rep, player_history) in players_details]

        # Will be the total number of contests the player has taken part in 
        # to the end of this round.
        self._total_number_contests_per_player += self.get_number_contests_this_round(player_reputations)
        
        return hunt_results

    def hunt_outcomes(self, food_earnings):
        # Payoff matrix from a single contest:

        # Me \ Them |     h     |     s     |
        # -----------------------------------
        #       h   |   0,  0   |   -3,  1  |
        # -----------------------------------
        #       s   |   1, -3   |   -2, -2  |
        # -----------------------------------

        # So we can use our food earnings from each contest in the round to 
        # identify whether each player in the contest hunted or slacked.
        players_choices = {-3:("h", "s"), -2:("s", "s"), 
                           0:("h", "h"), 1:("s", "h")}
        for i in range(len(food_earnings)):
            contest_choices = players_choices[food_earnings[i]]
            self._unknown_players_details[i]["choices_played"] = contest_choices


class RandomAntiSocialDetective(BaseDetective):
    '''Starts out as a modified Random: Player that hunts with probability 
    p_hunt and slacks with probability 1-p_hunt, as per Random.  However, 
    player will always slack against an opponent with either a high probability 
    of hunting or a low probability of hunting.
    As the game progresses and the reputations of the players become spread, 
    this player attempts to identify opponents via their reputations.  If it 
    can identify a player and match it to its choice (hunt or slack) from the 
    last round, then it will play a strategy against that player based on their 
    history while continuing to use the Random Anti-social strategy against 
    other players it can't identify.
    '''
    
    def __init__(self, name, p_hunt, antisocial_threshold, evil_threshold, 
                 single_hunt_choice_on_history, 
                 id = None, do_logging = False):
        # single_hunt_choice_on_history must have the signature:
        # single_hunt_choice_on_history(round_number, player_history)
        self.name = name

        assert p_hunt >= 0.00 and p_hunt <= 1.00, \
            "p_hunt must be at least 0 and at most 1"
        assert antisocial_threshold >= 0.00 and antisocial_threshold <= 1.00, \
            "antisocial_threshold must be at least 0 and at most 1"
        assert evil_threshold >= 0.00 and evil_threshold <= 1.00, \
            "evil_threshold must be at least 0 and at most 1"
        
        self.p_hunt = p_hunt
        self.antisocial_threshold = antisocial_threshold
        self.evil_threshold = evil_threshold
        self.single_hunt_choice_on_history = single_hunt_choice_on_history

        super(RandomAntiSocialDetective, self).__init__(self.name, 
                                                        self.single_hunt_choice, 
                                                        id, do_logging)

    def single_hunt_choice_probabilistic(self, round_number, player_rep):
        '''Performs a single hunt, returning either h (hunt) or s (slack), 
        if the history of the opponent is not known.
        '''
        random_threshold = self.p_hunt
        print ("prob hunt algorithm")
        if round_number == 1:
            return 'h'
        if player_rep >= self.antisocial_threshold:
            return 's'
        if player_rep < self.evil_threshold:
            return 's'
        if random.random() < random_threshold:
            return 'h'
        return 's'

    def single_hunt_choice(self, round_number, current_food, current_reputation, 
                             m, player_rep, player_history):
        '''Performs a single hunt, returning either h (hunt) or s (slack).
        '''
        if player_history is None or not player_history.has_key("choices_played"):
            return self.single_hunt_choice_probabilistic(round_number, player_rep)

        return self.single_hunt_choice_on_history(round_number, player_history)


class RandomAntiSocialGTFT(RandomAntiSocialDetective):
    '''Starts out as a modified Random: Player that hunts with probability 
    p_hunt and slacks with probability 1-p_hunt, as per Random.  However, 
    player will always slack against an opponent with either a high probability 
    of hunting or a low probability of hunting.
    As the game progresses and the reputations of the players become spread, 
    this player attempts to identify opponents via their reputations.  If it 
    can identify a player and match it to its choice (hunt or slack) from the 
    last round, then it will play the Generous-Tit-For-Tat strategy against 
    that player while continuing to use the Random Anti-social strategy against 
    other players it can't identify.
    '''
    
    def __init__(self, p_hunt, antisocial_threshold, evil_threshold, 
                 p_generosity, id = None, do_logging = False):
        self.name = "RASGeT{0}_{1}_{2}_{3}".format(p_hunt, 
                                                   antisocial_threshold, 
                                                   evil_threshold, 
                                                   p_generosity)

        assert p_generosity >= 0.00 and p_generosity <= 1.00, \
            "p_generosity must be at least 0 and at most 1"

        self.p_generosity = p_generosity

        super(RandomAntiSocialGTFT, self).__init__(self.name, p_hunt, 
                                                   antisocial_threshold, 
                                                   evil_threshold, 
                                                   self.single_hunt_choice_GTFT, 
                                                   id, do_logging)

    def single_hunt_choice_GTFT(self, round_number, player_history):
        '''Performs a single hunt, returning either h (hunt) or s (slack), 
        if the history of the opponent is known.  Follows a Generous Tit-For-Tat 
        strategy: Play what the opponent did last round, except if the opponent 
        played 's' then have a low probability of playing 'h'.  This is to avoid 
        the situation where if the opponent is playing a Tit-For-Tat-like 
        strategy both players could end up locked into always playing 's' 
        whenever they compete against each other.
        player_history is a dictionary which should have a key "choices_played", 
        representing the choices played by this player and this opponent in the 
        last round.
        '''
        print ("GTFT hunt algorithm")
        if round_number == 1:
            return 'h'
        choices_played_last_round = player_history["choices_played"]
        if choices_played_last_round[1] == 's':
            if random.random() < self.p_generosity:
                return 'h'
            return 's'
        return 'h'


class RandomAntiSocialPavlov(RandomAntiSocialDetective):
    '''Starts out as a modified Random: Player that hunts with probability 
    p_hunt and slacks with probability 1-p_hunt, as per Random.  However, 
    player will always slack against an opponent with either a high probability 
    of hunting or a low probability of hunting.
    As the game progresses and the reputations of the players become spread, 
    this player attempts to identify opponents via their reputations.  If it 
    can identify a player and match it to its choice (hunt or slack) from the 
    last round, then it will play the Pavlov strategy (also called the Win-Stay, 
    Lose-Switch strategy) against that player while continuing to use the 
    Random Anti-social strategy against other players it can't identify.
    '''
    
    def __init__(self, p_hunt, antisocial_threshold, evil_threshold, 
                 id = None, do_logging = False):
        self.name = "RASPav{0}_{1}_{2}".format(p_hunt, 
                                                   antisocial_threshold, 
                                                   evil_threshold)

        super(RandomAntiSocialPavlov, self).__init__(self.name, p_hunt, 
                                                   antisocial_threshold, 
                                                   evil_threshold, 
                                                   self.single_hunt_choice_pavlov, 
                                                   id, do_logging)

    def single_hunt_choice_pavlov(self, round_number, player_history):
        '''Performs a single hunt, returning either h (hunt) or s (slack), 
        if the history of the opponent is known.  Follows a Pavlov strategy 
        (also called the Win-Stay, Lose-Switch strategy): If the player won the 
        last contest against the same opponent then it should repeat the same 
        choice when playing the same opponent again.  If the player lost the 
        last contest then it should switch choices this time.  Winning is 
        defined as either both players hunting, or the opponent hunted while 
        this player slacked.  ie Winning = other player hunted last round.
        Losing is defined as either both players slacking, or the opponent 
        slacked while this player hunted.  ie Losing = other player slacked 
        last round.
        player_history is a dictionary which should have a key "choices_played", 
        representing the choices played by this player and this opponent in the 
        last round.
        '''
        print ("Pavlov hunt algorithm")
        if round_number == 1:
            return 'h'
        choices_played_last_round = player_history["choices_played"]
        I_played_last_round = choices_played_last_round[0]
        they_played_last_round = choices_played_last_round[1]
        if they_played_last_round == 's':
            if I_played_last_round == 's':
                return 'h'
            else:
                return 's'
        else:
            return I_played_last_round


class RandomAntiSocialPavlov2(BaseDetective):
    '''Starts out as a modified Random: Player that hunts with probability 
    p_hunt and slacks with probability 1-p_hunt, as per Random.  However, 
    player will always slack against an opponent with either a high probability 
    of hunting or a low probability of hunting.
    As the game progresses and the reputations of the players become spread, 
    this player attempts to identify opponents via their reputations.  If it 
    can identify a player and match it to its choice (hunt or slack) from the 
    last round, then it will play the Pavlov strategy (also called the Win-Stay, 
    Lose-Switch strategy) against that player while continuing to use the 
    Random Anti-social strategy against other players it can't identify.
    '''
    
    def __init__(self, p_hunt, antisocial_threshold, evil_threshold, 
                 id = None, do_logging = False):
        self.name = "RASPav2{0}_{1}_{2}".format(p_hunt, 
                                                   antisocial_threshold, 
                                                   evil_threshold)

        assert p_hunt >= 0.00 and p_hunt <= 1.00, \
            "p_hunt must be at least 0 and at most 1"
        assert antisocial_threshold >= 0.00 and antisocial_threshold <= 1.00, \
            "antisocial_threshold must be at least 0 and at most 1"
        assert evil_threshold >= 0.00 and evil_threshold <= 1.00, \
            "evil_threshold must be at least 0 and at most 1"
        
        self.p_hunt = p_hunt
        self.antisocial_threshold = antisocial_threshold
        self.evil_threshold = evil_threshold

        super(RandomAntiSocialPavlov2, self).__init__(self.name, 
                                                      self.single_hunt_choice, 
                                                      id, do_logging)

    def single_hunt_choice_pavlov(self, round_number, player_history, 
                                  player_rep):
        '''Performs a single hunt, returning either h (hunt) or s (slack), 
        if the history of the opponent is known.  Follows a Pavlov strategy 
        (also called the Win-Stay, Lose-Switch strategy): If the player won the 
        last contest against the same opponent then it should repeat the same 
        choice when playing the same opponent again.  If the player lost the 
        last contest then it should switch choices this time.  Winning is 
        defined as either both players hunting, or the opponent hunted while 
        this player slacked.  ie Winning = other player hunted last round.
        Losing is defined as either both players slacking, or the opponent 
        slacked while this player hunted.  ie Losing = other player slacked 
        last round.
        player_history is a dictionary which should have a key "choices_played", 
        representing the choices played by this player and this opponent in the 
        last round.
        '''
        print ("Pavlov hunt algorithm")
        if round_number == 1:
            return 'h'
        if player_rep < self.evil_threshold:
            return 's'

        choices_played_last_round = player_history["choices_played"]
        I_played_last_round = choices_played_last_round[0]
        they_played_last_round = choices_played_last_round[1]
        if they_played_last_round == 's':
            if I_played_last_round == 's':
                return 'h'
            else:
                return 's'
        else:
            return I_played_last_round

    def single_hunt_choice_probabilistic(self, round_number, player_rep):
        '''Performs a single hunt, returning either h (hunt) or s (slack), 
        if the history of the opponent is not known.
        '''
        random_threshold = self.p_hunt
        print ("prob hunt algorithm")
        if round_number == 1:
            return 'h'
        if player_rep >= self.antisocial_threshold:
            return 's'
        if player_rep < self.evil_threshold:
            return 's'
        if random.random() < random_threshold:
            return 'h'
        return 's'

    def single_hunt_choice(self, round_number, current_food, current_reputation, 
                             m, player_rep, player_history):
        '''Performs a single hunt, returning either h (hunt) or s (slack).
        '''
        if player_history is None or not player_history.has_key("choices_played"):
            return self.single_hunt_choice_probabilistic(round_number, player_rep)

        return self.single_hunt_choice_pavlov(round_number, player_history, 
                                                  player_rep)