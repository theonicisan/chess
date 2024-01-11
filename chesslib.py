def play_game(in_board, training=None):
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
    board_array = board_to_array(board)
    #replay_buffer = np.zeros([1,9,8,12], dtype=int)
    replay_buffer = np.expand_dims(board_array, axis=0)

    while not board.is_checkmate() and not board.is_stalemate() and not board.is_insufficient_material() and not board.can_claim_draw()    :
        i_count+=1
        all_moves = str(board.legal_moves)
        start_pos = [pos for pos, char in enumerate(all_moves) if char == '(']
        end_pos = [pos for pos, char in enumerate(all_moves) if char == ')']
        all_moves_string= all_moves[start_pos[0]+1:end_pos[0]]
        all_moves_string = all_moves_string.replace(" ", "")
        all_moves_array = all_moves_string.split(',')
        next_move = random.choice(all_moves_array)
        board.push_san(next_move)
        board_array = board_to_array(board)
        replay_buffer = np.append(replay_buffer, np.expand_dims(board_array, axis=0), axis=0)
    
    return board, replay_buffer

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
        out_board, _, _ = play_game(None)
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

def board_to_array(in_board):

    import chess
    import numpy as np
    # INPUTS
    # in_board of type chess.board()

    # OUTPUTS
    # board_array of type np.array(9,8,12)

    board_array = np.zeros([9,8,12], dtype=int)
    board = chess.Board()
    board = in_board

    board_string = str(board.outcome)
    board_string= board.fen()
    end_pos = [pos for pos, char in enumerate(board_string) if char == " "]
    meta_string = board_string[end_pos[0]+1:]
    board_string= board_string[0:end_pos[0]]
    rank_array = board_string.split('/')

    for r in range(8):
        rank_string = rank_array[r]
        f = 0 # initialize the manual file counter. 
        for character in (rank_string):
            # Because f is not always 8, we need a new iterator here to fill the entire rank.

            if character.isdigit():
                spaces = int(character)
                for e in range(spaces):
                    #print('dot')
                    f += 1

            elif character == 'r':   #assign black rooks
                board_array[r][f][0] = 1
                f += 1

            elif character == 'n':   #assign black knights
                board_array[r][f][1] = 1
                f += 1

            elif character == 'b':   #assign black bishops
                board_array[r][f][2] = 1
                f += 1
                
            elif character == 'q':   #assign black queens
                board_array[r][f][3] = 1
                f += 1

            elif character == 'k':   #assign black king
                board_array[r][f][4] = 1
                f += 1

            elif character == 'p':   #assign black pawns
                board_array[r][f][5] = 1
                f += 1

            elif character == 'R':   #assign white rooks
                board_array[r][f][7] = 1
                f += 1

            elif character == 'N':   #assign white knights
                board_array[r][f][8] = 1
                f += 1

            elif character == 'B':   #assign white bishops
                board_array[r][f][9] = 1
                f += 1

            elif character == 'Q':   #assign white queens
                board_array[r][f][10] = 1
                f += 1

            elif character == 'K':   #assign white king
                board_array[r][f][11] = 1
                f += 1

            elif character == 'P':   #assign white pawns
                board_array[r][f][6] = 1
                f += 1


    # populate the meta rank

    board_array[8][0][0] = board.fullmove_number

    for character in (meta_string):
        if character == 'w':
            board_array[8][0][1] = 1 # 1 if white is to move, 0 if black is to move
        elif character == 'K':
            board_array[8][0][2] = 1 # 1 if white can castle King side.
        elif character == 'Q':
            board_array[8][0][3] = 1 # 1 if white can castle Queen side.
        elif character == 'k':
            board_array[8][0][4] = 1 # 1 if black can castle King side.
        elif character == 'q':
            board_array[8][0][5] = 1 # 1 if white can castle Queen Side.
        elif board.is_checkmate():
            board_array[8][0][6] = 1 # 1 if board is checkmate.
        elif board.is_variant_draw() or board.can_claim_draw() or board.is_insufficient_material() or board.is_stalemate() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
            board_array[8][0][7] = 1 # 1 if board is draw

    return board_array

def board_is_terminal(in_board):
    import chess
    # INPUTS
    # in_board of type chess.board()

    # OUTPUTS
    # is_terminal as Boolean
    # reward as int

    board = chess.Board()
    board = in_board

    if board.is_variant_draw() or board.can_claim_draw() or board.is_insufficient_material() or board.is_stalemate() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        is_terminal = True
        reward = 0
    elif board.is_checkmate():
        is_terminal = True
        if board.turn:
            reward = -1
        else:
            reward = 1
    else:
        is_terminal = False
        reward = None

    return is_terminal, reward