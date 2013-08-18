from Player import BasePlayer
import random

class BaseAntiSocial(BasePlayer):
    '''Base class for the AntiSocial players. Player will always slack against 
    an opponent with either a high probability of hunting or a low probability 
    of hunting.
    '''
    
    def __init__(self, name, antisocial_threshold, evil_threshold, random_threshold, 
                 id = None, do_logging = False):
        self.name = name
        super(BaseAntiSocial, self).__init__(self.name, id, do_logging)

        assert antisocial_threshold >= 0.00 and antisocial_threshold <= 1.00, \
            "antisocial_threshold must be at least 0 and at most 1"
        assert evil_threshold >= 0.00 and evil_threshold <= 1.00, \
            "evil_threshold must be at least 0 and at most 1"

        self.antisocial_threshold = antisocial_threshold
        self.evil_threshold = evil_threshold
        self.random_threshold = random_threshold

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):

        def single_hunt_choice(player_rep):

            if self.random_threshold == "reputation":
                random_threshold = player_rep
            else: 
                random_threshold = self.random_threshold

            if round_number == 1:
                return 'h'
            if player_rep >= self.antisocial_threshold:
                return 's'
            if player_rep < self.evil_threshold:
                return 's'
            if random.random() < random_threshold:
                return 'h'
            return 's'

        return [single_hunt_choice(player_rep) for player_rep in player_reputations]

class RandomAntiSocial(BaseAntiSocial):
    '''Modified Random: Player that hunts with probability p_hunt and
    slacks with probability 1-p_hunt, as per Random.  However, player will 
    always slack against an opponent with either a high probability of hunting 
    or a low probability of hunting.
    '''
    
    def __init__(self, p_hunt, antisocial_threshold, evil_threshold, 
                 id = None, do_logging = False):

        self.name = "RandomAntiSocial{0}_{1}_{2}".format(
                                                     p_hunt, 
                                                     antisocial_threshold, 
                                                     evil_threshold)

        super(RandomAntiSocial, self).__init__(self.name, antisocial_threshold, 
                                               evil_threshold, p_hunt, 
                                               id, do_logging)

        assert p_hunt >= 0.00 and p_hunt <= 1.00, \
            "p_hunt must be at least 0 and at most 1"


class FairHunterAntiSocial(BaseAntiSocial):
    '''Modified FairHunter: Player that tries to be fair by hunting with same 
    probability as each opponent, as per FairHunter.  However, player will 
    always slack against an opponent with either a high probability of hunting 
    or a low probability of hunting.'''

    def __init__(self, antisocial_threshold, evil_threshold, 
                 id = None, do_logging = False):

        self.name = "FairHunterAntiSocial{0}_{1}".format(
                                                     antisocial_threshold, 
                                                     evil_threshold)

        super(FairHunterAntiSocial, self).__init__(self.name, antisocial_threshold, 
                                                   evil_threshold, "reputation", 
                                                   id, do_logging)
