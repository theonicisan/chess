# chess

It's been about a month since I started this project.  The objective was to better understand the chess algorithms that drive the popular chess engines out there.

First, some updates.
1. I have managed to implement the Python chess library as a framework for rules-management, and it provides me with board meta-data as well as generates legal moves.
2. My program then plays games in the style of Monte Carlo Simulations using random next moves until the board reaches a terminal state (checmate or draw).
3. As the simulations are played, each board is transalated into a 9x8x12 matrix where the first 8 rows of the matrix holds a one-hot-encoded board, and the 9th row holds meta-data of the board (i.e. castling rights, move count, critical state etc.).
4. The program also accumlates the board states into a nx9x8x12 matrix as a replay-buffer, which is written out to a .npy file after each game simulation.  This will later be used to train the Q(s,a) function.

Next steps.
1. Create a database that takes the board states (unraveled matrix), actions and assigns a calculated Q(s,a) value based on the reward (1, 0, -1) and the move count (used to incorporate the gamma-discount factor).
2. Construct a neural network (Tensorflow) to train the Q(s,a) function based on the training data derived from the simulated games.
3. Develop a training harness where the one player plays a random game (Monte Carlo) and the other player uses Q(s,a) function to pick a next move.  Ideally this will consistently result in a win-bias for the non-random player.

Challenges I am figuring out:
1. What database to use for the training / test data for the neural network.

