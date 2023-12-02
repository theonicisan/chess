# Design

The idea is to encapsulate the GAME as a vector matrix where:
  1. Dimension 0: Move number array (note that there is no grouping of moves so that move 1 includes a white and black move as per convention).  The dimension increments with every move made. Move 0 is always the setting of the board to the starting position.
  2. Dimension 1: Rank array (8 ranks).
  3. Dimension 2: File array (8 files).
  4. Dimension 3: One-hot-encoded array for the piece occupying the squeare (rank-file combination).  Note every piece is unique so the one-hot-encoded array will have 2 (black or white) * (16 (starting pieces) + 8 (theoretical pawn promotions)) = 48 classes.

Feature Vector (seperate from game matrix).
  1. Dimension 0: Pieces. 
  2. Dimension 1: Feature array (arbitrary - 10) containing binary-one-hot-encoding for:
     0. Active Indicator (1 if yes, 0 if no) - if a piece is taken, indicator changes from 1 to 0.
     1. First Move Indicator (1 if yes, 0 if no) - upon its first move, the indicator changes from 0 to 1. This is useful for pawn first-moves or castling.
     2. Piece Color (0 if black, 1 if white) - as this cannot change throughout the game, this is informational only.
     3. Is King (0 if no, 1 if yes).  Cannot change once set.
     4. Is Queen (0 if no, 1 if yes).  Cannot change once set.
     5. Is White Bishop (0 if no, 1 if yes).  Cannot change once set.
     6. Is Black Bishop (0 if no, 1 if yes).  Cannot change once set.
     7. Is Knight (0 if no, 1 if yes).  Cannot change once set.
     8. Is Rook (0 if no, 1 if yes).  Cannot change once set.
     9. Is Pawn (0 if no, 1 if yes).  Can change upon pawn promotion.
     10. Promoted (0 if no, 1 if yes).  Changes from 0 to 1 upon pawn promotion.

Once a GAME is encoded in a vector matrix, a collection of games can be assembled as a higher level vector.

After every move, the chess_game vector of shape (moves, rank(8), file(8), one-hot-encoded piece identifier(32)) will receive another move.

As the chess_game has moves appended, the feature vector will have to be updated.  I am not sure if it is worth "hand crafting" the feature vector or whether I should use a learning algorith to discover and embed features of every move/state of the board.  I am not a fan of teaching algorithms deterministic rules.  Perhaps the features can be split into deterministic features and learnt features.

It seems inevitable that the engine will have to be trained using a learning algorithm.  Some of the algorithms I have looked at seem to use reinforcement learning.  I was hoping to use CNN/RNN/Transformer Model principles where the board-state are treated as "words".  Each state could then be trained to have a feature embedding of deterministic and learned features.  This should assist in recommending a next move (or board-state).

Deterministic features could include:
1. Per Square
  1. Whether the piece is threatened or not.
  2. Whether the piece is "hanging" or not.

     
