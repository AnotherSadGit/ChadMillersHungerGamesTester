from Player import BasePlayer

class ThresholdPlayer(BasePlayer):
    '''Hunter in the Brilliant.org Hunger Games which ignores m and just plays 
    the prisoner's dilemma.  It compares a test value to a threshold and plays 
    'h' if the test value is above the threshold or 's' if the value is below 
    it.
    '''

    def __init__(self, first_hunt_function, threshold, test_value, bias = 0, do_logging = False):
        super(ThresholdPlayer, self).__init__(do_logging)
        '''Sets up the parameters that define how the player will hunt during 
        the game.

        Arguments:
        1) first_hunt_function - function: Function that specifies how the 
        player will play in a single contest on the first round.  Returns 
        either 'h' or 's'.
        2) threshold - numeric or string: The threshold that determines 
        whether the player will play 'h' or 's'.  Normally numeric but may take 
        special string values that represent a varying threshold, eg the 
        reputation of the opposing player.
        3) test_value - numeric or string: The value that is compared to the 
        threshold to determine whether the player will play 'h' or 's'.  
        May be numeric or may take special string values that represent a 
        varying value, eg the reputation of the opposing player.
        4) bias - numeric: A value that can be added to the threshold to bias 
        the player towards hunting more or slacking more.
        '''

        # Ever so slightly biased, since if the threshold is 0.5,
        # 0 <= s < 0.5 and 0.5 <= h <= 1.0
        # (ie there are slightly more values in range H than in range S).        
        def single_hunt_function(round_number, current_food, current_reputation,
                                 m, other_player_reputation):
            
            if threshold == "reputation":
                decision_threshold = (1 - other_player_reputation)
            else:
                decision_threshold = threshold
               
            if test_value == "reputation":
                value_to_test = other_player_reputation
            elif test_value == "random":
                value_to_test = random.random()
            else:
                value_to_test = test_value
               
            # ASSUMPTION: First round is numbered 1, not 0.
            if round_number == 1:
                return first_hunt_function(round_number, current_food,
                                           current_reputation, m,
                                           other_player_reputation,
                                           decision_threshold, value_to_test)
            elif value_to_test < (decision_threshold + bias):
                return "s"
            else:
                return "h"
        
        self._single_hunt_function = single_hunt_function


    def _first_hunt_fixed_value(self, h_or_s):
        def first_hunt_function(round_number, current_food, current_reputation, 
                                m, other_player_reputation, threshold, test_value):
            return h_or_s
        return first_hunt_function


    def _first_hunt_threshold_value(self, threshold, test_value):
        def first_hunt_function(round_number, current_food, current_reputation, 
                                m, other_player_reputation, threshold, test_value):
            return ("s" if test_value < threshold else "h")
        return first_hunt_function
    

    def hunt_choices(self, round_number, current_food, current_reputation,
                    m, player_reputations):
        '''Play a round of the Hunger Games against each of the other players.

        Arguments:
        1) round_number - integer: Number of the current round of the game;
        2) current_food - integer: The number of remaining food points the
        player has at the start of the current round;
        3) current_reputation - float: Reputation the player has at the start
        of the current round.  On the first round this is expected to be 0;
        4) m - integer: The food threshold for the current round (the number of
        hunts required in the current round for all players to gain bonus
        food);
        5) player_reputations - list of floats: The reputations of the other 
        players competing in the current round, in random order.  On the first 
        round this is expected to be 0 for each player.

        Return:
        round_results - list of strings: For each of the other players 
        in player_reputations, the corresponding element in round_results will 
        be either "h" (Hunt) or "s" (Slack), indicating this player will 
        either hunt or slack when hunting with that other player.

        '''
        hunt_results = [self._single_hunt_function(round_number,
                                                   current_food,
                                                   current_reputation,
                                                   m, rep)
                        for rep in player_reputations]
        return hunt_results        


    def hunt_outcomes(self, food_earnings):
        '''Required function defined in the rules'''
        pass        


    def round_end(self, award, m, number_hunters):
        '''Required function defined in the rules'''
        pass


class FixedThreshold(ThresholdPlayer):
    '''Hunter in the Brilliant.org Hunger Games which ignores m and just plays 
    the prisoner's dilemma.  It compares the other player's reputation to a 
    fixed threshold and plays 'h' if the other player's reputation is above the 
    threshold or 's' if it's below it.
    '''

    def __init__(self, threshold, first_hunt_value, do_logging = False):
        self.name = "FixedThreshold" + str(threshold) + first_hunt_value
        first_hunt_function = super(FixedThreshold,
                                    self)._first_hunt_fixed_value(first_hunt_value)
        test_value = "reputation"
        super(FixedThreshold, self).__init__(first_hunt_function, 
                                             threshold, test_value, 
                                             do_logging = do_logging)