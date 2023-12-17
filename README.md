# chess

It's been about a month since I started this project.  The objective was to better understand the chess algorithms that drive the popular chess engines out there.

First, some updates.
I have managed to use the Python chess library as a framwork as it saves me re-inventing the wheel.  I use it to generate legal moves and determine terminal states of the board.
With a couple of lines of code, I could then put together a Monte Carlo simulation that plays completely random moves from the list of available moves.  Below is an example of a completely random outcome after 10,000 games simulated on my latop (i5 with no GPU).  
1. From a number of simulations, the wins for black and white remained fairly close to each other.  I initially thought that White would have an advantage as the first-mover, but the simulations did not support this assumption.
2. The average number of moves per game remained very stable.  Keep in mind that critical states included checkmate, insufficient material, stalemate, repetition as well as the 50 and 75 move rules.
3. The number of winning outcomes (checkmate for either black or white) was always around ~15%.

    Number of games played: 10,000
    Number of wins for WHITE: 751
    Number of wins for BLACK: 783
    Number of draws: 8,466
    Average Moves per Game: 165
    Average time per game: 0.497sec

Next steps.
Seeing as I now have a baseline of around 7% for a win if moves are randomly made, all the algorithm has to do is to consistenly improve on 7%.
The algorith that makes sense to use is a Reinforcement Learning algorithm, more specifically Q-learning algorithm using Bellman's Equation for Q(a,s).  I aim to use a Monte Carlo simulation to generate a training dataset and a Tensorflow neural network to train for Q(a,s) using simulated play outcomes where a rewards are 1 (win), 0 (draw) and -1 (lose).

Seeing as I have very limited infrastructure to train with, I would like to use a Critical State solver (an algorithm that checks if there is a forced-mate possibility for the board state) instead of playing games to conclusion.  Such algorithms don't seem to be generally available.

Challenges I am figuring out:
1. The vector shapes for the neural network.  I was hoping to use a 8x8x32 vector that represents the board and a one-hot-encoded value for every square representing a piece identifier.  This 3x3x32 shape could be the input vector or state (s) as well as the action vector (a).
2. As I don't have much memory, I need to find a way to persist a large training set.  Seeing as the tree-search will depend on a position already having been visited, I would need to be able to store about 10,000 (games) * 160 (moves) * 2 (half-moves) * 3x3x32 states.

