:: Test Tournament for the Hunger Games Game Theory Programming Tournament
:: =======================================================================
:: Simon Elms, 16 Aug 2013

:: Tournament details:  https://brilliant.org/competitions/hunger-games/
:: Tournament app forked from Chad Miller's Hunger Games repo: https://github.com/ChadAMiller/hungergames.git

python app.py --pushover 3,0 --freeloader 3,0 --alternator 3,0 --max-rep-hunter 3,0 --fair-hunter 3,0 --avg-hunter 3,0 --random 3,0.25,0  3,0.4,0  3,0.6,0  3,0.75,0 --bounded-hunter 3,0.6,1.0,0  3,0.75,1.0,0 --fixed-threshold 3,0.4,h,0  3,0.4,s,0  3,0.6,h,0  3,0.6,s,0 --random-antisocial 3,0.8,0.9,0.1,0  3,0.8,0.9,0.0,0 --fair-hunter-antisocial 3,0.9,0.1,1  3,0.9,0.0,1

pause