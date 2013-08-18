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
    Your strategy starts here.
    '''
    
    def __init__(self, id = None, do_logging = False):
        super(Player, self).__init__(id, do_logging)
        self.name = "Nasty"

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):
        '''Required function defined in the rules'''
                    
        return ['s']*len(player_reputations)
        

    def hunt_outcomes(self, food_earnings):
        '''Required function defined in the rules'''
        pass
        

    def round_end(self, award, m, number_hunters):
        '''Required function defined in the rules'''
        pass
        
