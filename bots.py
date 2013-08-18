from Player import BasePlayer
import random

class Pushover(BasePlayer):
    '''Player that always hunts.'''

    def __init__(self, id = None, do_logging = False):
        self.name = "Pushover"
        super(Pushover, self).__init__(self.name, id, do_logging)
        
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['h']*len(player_reputations)

        
class Freeloader(BasePlayer):
    '''Player that always slacks.'''
    
    def __init__(self, id = None, do_logging = False):
        self.name = "Freeloader"
        super(Freeloader, self).__init__(self.name, id, do_logging)
    
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['s']*len(player_reputations)
        

class Alternator(BasePlayer):
    '''Player that alternates between hunting and slacking.'''

    def __init__(self, id = None, do_logging = False):
        self.name = "Alternator"
        super(Alternator, self).__init__(self.name, id, do_logging)
        self.last_played = 's'
        
    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        hunt_decisions = []
        for i in range(len(player_reputations)):
            self.last_played = 'h' if self.last_played == 's' else 's'
            hunt_decisions.append(self.last_played)

        return hunt_decisions

class MaxRepHunter(BasePlayer):
    '''Player that hunts only with people with max reputation.'''

    def __init__(self, id = None, do_logging = False):
        self.name = "MaxRepHunter"
        super(MaxRepHunter, self).__init__(self.name, id, do_logging)

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        threshold = max(player_reputations)
        return ['h' if rep == threshold else 's' for rep in player_reputations]


class Random(BasePlayer):
    '''
    Player that hunts with probability p_hunt and
    slacks with probability 1-p_hunt
    '''
    
    def __init__(self, p_hunt, id = None, do_logging = False):
        self.name = "Random" + str(p_hunt)
        super(Random, self).__init__(self.name, id, do_logging)
        assert p_hunt >= 0.00 and p_hunt <= 1.00, "p_hunt must be at least 0 and at most 1"
        self.p_hunt = p_hunt

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['h' if random.random() < self.p_hunt else 's' for p in player_reputations]

class FairHunter(BasePlayer):
    '''Player that tries to be fair by hunting with same probability as each opponent'''

    def __init__(self, id = None, do_logging = False):
        self.name = "FairHunter"
        super(FairHunter, self).__init__(self.name, id, do_logging)

    def hunt_choices(
                self,
                round_number,
                current_food,
                current_reputation,
                m,
                player_reputations,
                ):
        return ['h' if random.random() < rep else 's' for rep in player_reputations]
        
class BoundedHunter(BasePlayer):
    '''Player that hunts whenever the other's reputation is within some range.'''

    def __init__(self, lower, upper, id = None, do_logging = False):
        self.name = "BoundedHunter" + str(lower)+'-'+str(upper)
        super(BoundedHunter, self).__init__(self.name, id, do_logging)
        self.low = lower
        self.up = upper

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        return ['h' if self.low <= rep <= self.up else 's' for rep in player_reputations]
        
class AverageHunter(BasePlayer):
    '''Player that tries to maintain the average reputation, but spreads its hunts randomly.'''
    
    def __init__(self, id = None, do_logging = False):
        self.name = "AverageHunter"
        super(AverageHunter, self).__init__(self.name, id, do_logging)

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        avg_rep = sum(player_reputations) / float(len(player_reputations))
        return ['h' if random.random() < avg_rep else 's' for rep in player_reputations]