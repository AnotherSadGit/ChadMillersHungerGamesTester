from Player import BasePlayer
import copy

class DectectivePlayer(BasePlayer):
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

    def __init__(self, id = None, do_logging = False):
        super(DectectivePlayer, self).__init__(id, do_logging)
        self.name = "DectectivePlayer"

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
                                     total_contests_per_player_end_last_round):
        # The number of elements in players_reputations is 
        # (number_players_this_round - 1), as it does not include the 
        # reputation of the player represented by this class. 
        number_players_this_round = len(players_reputations_end_last_round) + 1
        unknown_players_details = \
            [{"prev_rep": rep, 
              "rep_forecasts": self.forecast_player_reputation(rep, 
                                                          total_contests_per_player_end_last_round, 
                                                          number_players_this_round)
                          } for rep in players_reputations_end_last_round]
        return unknown_players_details
    

    def identify_players(self, players_reputations_end_last_round):
        # It's possible to have two overlapping forecast reputation ranges, 
        # which have two actual player reputations in them.  If one 
        # forecast reputation range has only one actual reputation in it then a 
        # player has been identified.  If the other forecast reputation range 
        # has two actual reputations in it then a player cannot be identified.
        # However, if one of the two actual reputations is found to match the 
        # other overlapping forecast reputation range, it can be eliminated 
        # since it matches the other forecast reputation range.  Then only one 
        # actual reputation is left and it can be matched to the second 
        # forecast rule.
        # So repeat the match process as long as at least one match is found in 
        # the previous pass through the loop.
        players_reps = copy.deepcopy(players_reputations_end_last_round)
        match_found = True
        while match_found:
            match_found = False
            for player in self._unknown_players_details:
                matching_reputations = [rep for rep in players_reps
                                        if rep >= player["rep_forecasts"][0]
                                        and rep <= player["rep_forecasts"][1]]
                if len(matching_reputations) == 1:
                    match_found = True
                    player["matching_index"] = players_reps.index(matching_reputations[0])  
                    del players_reps[player["matching_index"]]


    def hunt_choices(self, round_number, current_food, current_reputation, m,
            player_reputations):
        self.identify_players(player_reputations)
        known_players = [player for player in self._unknown_players_details 
                         if player.has_key("matching_index")]
        # Record the player details to be used to identify players in the next round.
        self._unknown_players_details = \
            self.forecast_players_reputations(player_reputations, 
                                              self._total_number_contests_per_player)

        # Play the contests here.

        # Will be the total number of contests the player has taken part in 
        # to the end of this round.
        self._total_number_contests_per_player += get_number_contests_this_round(player_reputations)
                

    def hunt_outcomes(self, food_earnings):
        # Payoff matrix from a single contest:

        # Me \ Them |     h     |     s     |
        # -----------------------------------
        #       h   |   0,  0   |   -3,  1  |
        # -----------------------------------
        #       s   |   1, -3   |   -2, -2  |
        # -----------------------------------

        # So we can use the food earnings from each contest in the round to 
        # identify whether each player in the contest hunted or slacked.
        players_choices = {-3:("h", "s"), -2:("s", "s"), 
                           0:("h", "h"), 1:("s", "h")}
        for i in range(len(food_earnings)):
            contest_choices = players_choices[food_earnings[i]]
            self._unknown_players_details[i]["choices_played"] = contest_choices