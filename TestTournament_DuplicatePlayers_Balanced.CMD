:: Test Tournament for the Hunger Games Game Theory Programming Tournament
:: =======================================================================
:: Simon Elms, 16 Aug 2013

:: Tournament details:  https://brilliant.org/competitions/hunger-games/
:: Tournament app forked from Chad Miller's Hunger Games repo: https://github.com/ChadAMiller/hungergames.git

:: Categorize players as nice, nasty, neutral or variable depending on whether they tend to hunt more or slack more, and whether the hunt/slack ratio can be varied or is fixed:

:: Nice players:
:: 1) Pushover: Always hunts;

:: Nasty players:
:: 1) Freeloader: Always slacks;
:: 2) MaxRepHunter: Only hunts if the other player has the maximum reputation, otherwise slacks;

:: Neutral players:
:: 1) Alternator: Alternates between slacking and hunting, so will have a rep of 0.5;

:: Variable players:
:: 1) FairHunter: Hunts with the same probability as its opponent (so will slack more if it has more nasty opponents);
:: 2) AverageHunter: Hunts with the average probability of all the players (so will slack more if it has more nasty 
::      opponents);
:: 3) Random: Hunts with a probability that is set when instantiated;
:: 4) BoundedHunter: Hunts when opponent's reputation is within a range set when instantiated;
:: 5) FixedThreshold: Hunts when opponent's reputation is above a threshold set when instantiated;
:: 6) RandomAntiSocial: Hunts with a probability that is set when instantiated but slacks if opponent's reputation is 
::      very high or very low;
:: 7) FairHunterAntiSocial: Hunts with the same probability as its opponent but slacks if opponent's reputation is 
::      very high or very low;

:: -----------------------------------------------------------------------
:: This test tournament: Duplicate players (multiple of the same type with 
:: identical parameters) and attempting to be balanced.  ie AverageHunter's
:: reputation should be approximately 0.5 after, say, 50 rounds (long
:: enough for reputations to settle down, short enough that players should 
:: not have been eliminated yet).
:: -----------------------------------------------------------------------
python app.py  --log-filename game_balanced.txt --pushover 3,0 --freeloader 3,0 --alternator 3,0 --max-rep-hunter 3,0 --fair-hunter 3,0 --avg-hunter 3,0 --random 3,0.5,0 --bounded-hunter 3,0.4,1.0,0  3,0.65,1.0,0 --fixed-threshold 3,0.3,h,0  3,0.3,s,0  3,0.6,h,0  3,0.6,s,0 --random-antisocial 3,0.8,0.9,0.1,0  3,0.8,0.9,0.0,0 --fair-hunter-antisocial 3,0.9,0.1,0  3,0.9,0.0,0

pause