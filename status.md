Short update on where I am with this.

Managed to use the chess library to build some building blocks.

The algorithm should be able to:
1. Take any board position and play it through to a winning outcome.
2. Then pick a game that is a winning outcome for that position and play the next move.
3. Then the other player should make a move.  The other player could be the digital twin that is playing against itself or just another random pick of the legal moves.
4. Then, in picking a next move, it should be able to look forward into the possible winning scenarios that the opponent can play against its own scanarios, and NOT play those scenarios provide they overlap at that stage.

The idea would be to now build a Monte-Carlo simulation of random chess games.

Here are the results of the first simulation over 1000 random games:
Number of games played: 1000
Number of checkmates for WHITE: 102
Number of checkmates for BLACK: 71
Number of draws: 827
Average Moves: 162.56056056056056
Total time: 541.9873287677765, average time per game: 0.5425298586264029