def play_game(in_board):
    # Plays a game from the starting position by selecting random moves from the available legal moves list.
    
    import chess
    import random
    import numpy as np

    board = chess.Board()
    if in_board is not None:
        board = in_board

    # Debugging only.
    i_count = 0
    #opening_position = 'dymmy' #board.peek()
    first_next_move = ''

    while not board.is_checkmate() and not board.is_stalemate() and not board.is_insufficient_material() and not board.can_claim_draw()    :
        i_count+=1
        all_moves = str(board.legal_moves)
        start_pos = [pos for pos, char in enumerate(all_moves) if char == '(']
        end_pos = [pos for pos, char in enumerate(all_moves) if char == ')']
        all_moves_string= all_moves[start_pos[0]+1:end_pos[0]]
        all_moves_string = all_moves_string.replace(" ", "")
        all_moves_array = all_moves_string.split(',')
        next_move = random.choice(all_moves_array)
        if i_count==1:
            first_next_move = next_move #board.turn is chess.BLACK
        board.push_san(next_move)
    
    return board, first_next_move

def simulate_play(iterations):
    
    import time
    import chess
    
    out_board = chess.Board()
    num_wins_white = 0
    num_wins_black = 0
    num_draws = 0
    num_stalemate = 0
    num_canclaimdraw = 0
    num_undefined = 0
    num_insufficient = 0
    num_games = iterations
    moves = 0
    result = ''


    # Simulate games as a kind of Monte-Carlo simulation for games played using random moves.

    start_time = time.time()

    for i in range(num_games):
        out_board, _ = play_game(None)
        moves += out_board.fullmove_number
        if out_board.is_variant_draw() or out_board.can_claim_draw() or out_board.is_insufficient_material() or out_board.is_stalemate() or out_board.is_seventyfive_moves() or out_board.is_fivefold_repetition() :
            num_draws += 1
        elif out_board.outcome().winner:
            num_wins_white += 1
        elif not out_board.outcome().winner:
            num_wins_black += 1
        elif out_board.is_stalemate():
            num_stalemate += 1
        elif out_board.can_claim_draw():
            num_canclaimdraw += 1
        elif out_board.is_insufficient_material():
            num_insufficient += 1
        else:
            num_undefined += 1 # Just used a control to check if all games were counted.

    end_time = time.time()
    duration_time = end_time - start_time
    average_time = duration_time / i
    moves = moves / i

    return num_wins_white, num_wins_black, num_draws, moves, average_time