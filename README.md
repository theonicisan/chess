# chess

Chess is a deterministic problem. Every game of chess that can ever be played can be simulated and because this is the case, any possible outcome from a specific state on the board can be modeled and evaluated.  It should therefore be possible to determine the best next move on the board at any given point in time.  If there is at least one solution to check-mate from a particular board state, it should be possible to force a win.

Whether there exists a deterministic path to a win from the first move is not clear.  Some research has shown that deterministic outcomes are possible to calculate but due to the prohibitive complexity, only simplified states (end-game states with a reduced number of remaining pieces on the board) have been modeled and recorded.  No research has been able to reach back far enough into the game to record or calculate the deterministic outcomes when the possible outcome-set is still prohibitively large.

As a result, a probabilistic approach to algorithmic chess has been popular.  
1. The probability of the best next move is computed based on a learned corpus of games.
2. Re-inforcement learning algorithms can also presumably be used to "map" the best sequence of moves.

This project will aim to:
1. Recreate existing paradigms of algorithmic chess - but only for research purposes.
2. Evaluate opportunities for improvement in existing paradigms.
3. Evaluate laternative paradigms.

As this problem has been the subject of significant research and development and is considered a mature and possibly exhausted field, I do not expect to find anything that has not been discovered yet.  This project is largely to stimulate curiosity on the topic.
