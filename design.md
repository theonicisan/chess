# Design

The idea is to encapsulate the GAME as a vector matrix where:
  1. Dimension 0: Move number array (note that there is no grouping of moves so that move 1 includes a white and black move as per convention).  The dimension increments with every move made. Move 0 is always the setting of the board to the starting position.
  2. Dimension 1: Rank array (8 ranks).
  3. Dimension 2: File array (8 files).
  4. Dimension 3: One-hot-encoded array for the piece occupying the squeare (rank-file combination).  Note every piece is unique so the one-hot-encoded array will have 2 (black or white) * (16 (starting pieces) + 8 (theoretical pawn promotions)) = 48 classes.
  5. Dimension 4: Feature array (arbitrary - 10) containing binary-one-hot-encoding for:
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
     
