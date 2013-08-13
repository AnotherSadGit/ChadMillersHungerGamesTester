from __future__ import division, print_function
import random
import sys
import os

from Player import Player

# Primary engine for the game simulation. You shouldn't need to edit
# any of this if you're just testing strategies.

def payout(s1,s2):
    if s1 == 'h':
        if s2 == 'h':
            return 0
        else:
            return -3
    else:
        if s2 == 'h':
            return 1
        else:
            return -2
            
            
class GamePlayer(object):
    '''
    Wrapper class for players to keep track of food etc
    Parent is the main game instance, so we can just ask
    how many hunts have happened.
    '''
    def __init__(self, parent, player, food, hunts=0):
        self.parent = parent
        self.player = player
        self.food = food
        self.hunts = hunts
        
    @property
    def rep(self):
        return self.hunts/self.parent.hunt_opportunities if self.parent.hunt_opportunities else 0
        
    def __repr__(self):
        return '{} {} {:.3f}'.format(self.player, self.food, self.rep)

    def __str__(self):
        return "Player {} now has {} food and a reputation of {:.3f}".format(self.player, self.food, self.rep)
        
            
    
class Game(object):
    '''
    Game(players, verbose=True, min_rounds=300, average_rounds=1000, end_early=False)
    
    Primary game engine for the sim. players should be a list of players
    as defined in Player.py or bots.py. verbose determines whether the game
    will print the result of individual rounds to the console or not.
    
    Per the rules, the game has a small but constant probability of ending
    each round after min_rounds. The current defaults are completely arbitrary;
    feel free to play with them.

    End_early is an option to allow you to better test your strategy.  If specified
    as True, the game will end if the 'Player' player is eliminated (in addition
    to ending if any of the other game end conditions are met).
        
    Call game.play_game() to run the entire game at once, or game.play_round()
    to run one round at a time.
    
    See app.py for a bare-minimum test game.
    '''   
    def __init__(self, players, verbose=True, min_rounds=300, average_rounds=1000, end_early=False, 
                 log_to_file=False, log_filename=None):
        self.verbose = verbose
        assert average_rounds > min_rounds, "average_rounds must be greater than min_rounds"
        self.max_rounds = min_rounds + int(random.expovariate(1/(average_rounds-min_rounds)))
        self.round = 0
        self.hunt_opportunities = 0
        self.end_early = end_early
        
        start_food = 300*(len(players)-1)
        
        self.players = [GamePlayer(self,p,start_food) for p in players]

        self.output_to_file = log_to_file
        self.output_stream = sys.stdout
        if self.output_to_file:
            # Open as file object rather than opening it via io.open as a text 
            # stream: A file object takes strings while a text stream takes 
            # unicode.  Unicode causes a problem when writing players' details.
            self.output_stream = open(log_filename, "wt")

        if self.verbose:
            print("Game parameters:\n # players: %d\n verbose: %s\n " \
                  "min_rounds: %d\n average_rounds: %d\n " \
                  "end_early: %s\n" % (len(players), verbose, \
                                       min_rounds, average_rounds,
                                       end_early), file = self.output_stream)

    def __del__(self):
        if self.output_to_file:
            try:
                self.output_stream.flush()
                os.fsync(self.output_stream.fileno())
            finally:
                self.output_stream.close()     

    @property
    def m_bonus(self):
        return 2*(self.P-1)
    
    @property
    def P(self):
        return len(self.players)
        
    def calculate_m(self):
            return random.randrange(1, self.P*(self.P-1))
            
        
    def play_round(self):
        # Get beginning of round stats        
        self.round += 1
        if(self.verbose):
            print ("\nBegin Round " + str(self.round) + ":",
                   file = self.output_stream)
        m = self.calculate_m()
        
        # Beginning of round setup
        random.shuffle(self.players)
        reputations = list(player.rep for player in self.players)
        
        # Get player strategies
        strategies = []
        for i,p in enumerate(self.players):
            opp_reputations = reputations[:i]+reputations[i+1:]
            strategy = p.player.hunt_choices(self.round, p.food, p.rep, m, opp_reputations)

            strategy.insert(i,'s')
            strategies.append(strategy)

        # Perform the hunts
        self.hunt_opportunities += self.P-1

        results = [[] for j in range(self.P)]
        for i in range(self.P):
            for j in range(self.P):
                if i!=j:
                    results[i].append(payout(strategies[i][j], strategies[j][i]))
                
        total_hunts = sum(s.count('h') for s in strategies)
        
        if (self.verbose):
            print ("There were {} hunts of {} needed for bonus".format(total_hunts, m),
                    file = self.output_stream)

        if total_hunts >= m:
            bonus = self.m_bonus
            if (self.verbose):
                print("Cooperation Threshold Achieved. Bonus of {} awarded to each player".format(self.m_bonus),
                      file = self.output_stream)
        else:
            bonus = 0
        
        # Award food and let players run cleanup tasks
        for strat, result, player in zip(strategies, results, self.players):
            food = sum(result)
            hunts = strat.count('h')
            
            player.food += food+bonus
            player.hunts += hunts
            player.player.hunt_outcomes(result)
            player.player.round_end(bonus, m, total_hunts)
            
    
        if self.verbose:
            newlist = sorted(self.players, key=lambda x: x.food, reverse=True)
            for p in newlist:
                print (p, file = self.output_stream)
                   
        
        if self.game_over():
            print ("", file = self.output_stream)
            print ("Game Completed after {} rounds".format(self.round),
                   file = self.output_stream)
            if self.output_to_file:
                print ("Game Completed after {} rounds".format(self.round))
            raise StopIteration            
        
    def game_over(self):        
        starved = [p for p in self.players if p.food <= 0]
        quit = False

        for p in starved:
            print ("{} has starved and been eliminated in round {}".format(p.player, self.round),
                   file = self.output_stream)

            if isinstance(p.player, Player) and self.end_early:
                quit = True

        self.players = [p for p in self.players if p.food > 0]
        
        return (self.P < 2) or (self.round > self.max_rounds) or quit
        
        
    def play_game(self):
        '''
        Preferred way to run the game to completion
        Written this way so that I can step through rounds one at a time
        '''
        print ("Playing the game to the end:", file = self.output_stream)

        while True:
            try:
                self.play_round()
            except StopIteration:

                if len(self.players) <= 0:
                    print ("Everyone starved", file = self.output_stream)
                elif (len(self.players) == 1):
                    print ("The winner is: ", self.players[0].player,
                           file = self.output_stream)
                else:
                    survivors = sorted(self.players, key=lambda player: player.food, reverse=True)
                    print ("The winner is: ", survivors[0].player,
                           file = self.output_stream)
                    print ("Multiple survivors:",
                           file = self.output_stream)
                    print (survivors, file = self.output_stream)

                if self.output_to_file:
                    try:
                        # Ensure the output buffer is flushed and written to 
                        # disk before finishing up, otherwise may miss the 
                        # details of the last few rounds.
                        self.output_stream.flush()
                        os.fsync(self.output_stream.fileno())
                    finally:
                        self.output_stream.close()
                break
        
