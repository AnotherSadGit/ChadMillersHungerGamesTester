import random

class BasePlayer(object):
    '''
    Base class that allows Player and other test classes to run in a 
    tournament simulator based on the one created by Chad Miller, at 
    https://github.com/ChadAMiller/hungergames.git

    While this code isn't needed for the tournament proper it can't hurt so 
    it's been left in.
    '''
    def __init__(self, name, id = None, do_logging = False):
        self.name = name
        self.id = id
        self.do_logging = do_logging

        # uid: Unique identifier.  If only one player of each type is 
        # included in the tournament then the object name is enough to 
        # uniquely identify the player.  If there are multiple players of 
        # a type, however, then to uniquely identify a given player we need 
        # name + id, where id is unique to a player in a group of players of 
        # the same type.  The uids are formatted so they can double as 
        # display names for the players.
        
        # eg Random[0], Random[1], Random[2]: 
        #   * the names are all "Random";
        #   * the ids are 0, 1, 2;
        #   * the uids are "Random[0]", "Random[1]", "Random[2]";
        #   * the sort_orders are "Random00000", "Random00001", "Random00002".

        if self.id is not None:
            self.uid = "{0}[{1}]".format(self.name, self.id)
            self.sort_order = "{0}{1:05}".format(self.name, self.id)
        else:
            self.uid = self.name
            self.sort_order = self.name


    def __str__(self):
        try:
            return self.uid
        except AttributeError:
            # Fall back on Python default
            return super(BasePlayer, self).__repr__()


    def hunt_choices(*args, **kwargs):
        raise NotImplementedError("You must define a strategy!")
        
    def hunt_outcomes(*args, **kwargs):
        pass
        
    def round_end(*args, **kwargs):
        pass


class Player(BasePlayer):
    '''
    Cynical Nice Guy: This strategy can be summarized as:

    1) In general, be a nice guy;
    2) but don't be a mug; 
    3) and take advantage of any easy marks you encounter.

    In detail:
    
    1) In general, be a nice guy: Hunt with a probability of 0.8, randomized.

    2) Don't be a mug: When up against a really evil competitor, with a really 
    low reputation, stop being a nice guy.  Always slack against such an evil 
    competitor.

    3) Take advantage of any easy marks: If a competitor always hunts, 
    then take advantage of them by slacking.

    In addition, start off hunting on the first round so that other players 
    will see a good reputation to start with, and won't punish this player in 
    the early rounds for having a low reputation.

    This strategy just plays to the prisoner's dilemma and ignores the public 
    goods game where all players get a bonus if enough hunt during a round.  
    Since bonuses are awarded to all players they benefit all players equally 
    so they can be ignored for the purposes of the game.  The only benefit to 
    playing to win a bonus would come after many rounds, when the player's food 
    points are low.  Then gaining a bonus would be helpful to allow the player 
    to live to fight another round.  However, increasing the probability of 
    hunting might make the player more vulnerable to losing food points to 
    slacker competitors.  Given that, and that simplicity when coding is next 
    to Godliness, we'll ignore the public goods game.
    '''
    
    def __init__(self, id = None, do_logging = False):
        self.name = "CynicalNiceGuy"
        self.p_hunt = 0.8
        self.antisocial_threshold = 0.9
        self.evil_threshold = 0.03

        super(Player, self).__init__(self.name, id, do_logging)


    def single_hunt_choice(self, round_number, player_rep):

        if round_number == 1:
            return 'h'
        if player_rep >= self.antisocial_threshold:
            return 's'
        if player_rep < self.evil_threshold:
            return 's'
        if random.random() < self.p_hunt:
            return 'h'
        return 's'


    def hunt_choices(self, round_number, current_food, current_reputation,
                     m, player_reputations):
        '''Required function defined in the rules'''
        return [self.single_hunt_choice(round_number, player_rep) 
                for player_rep in player_reputations]
        

    def hunt_outcomes(self, food_earnings):
        '''Required function defined in the rules'''
        pass
        

    def round_end(self, award, m, number_hunters):
        '''Required function defined in the rules'''
        pass
        
