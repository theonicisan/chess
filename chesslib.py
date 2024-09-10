# Chess Library

# Imports
import chess
import random
import time
from teradataml import *


def play_game(in_board, game_id, training=None):
    
    # Initialize the starting variables.
    sequence_no = 0
    reward = 0
    
    game_df = pd.DataFrame({
        'game_id': [],
        'ply': [],
        'FEN': [],
        'move': [],
        'reward': [],
    })
    board = chess.Board()
    if in_board is not None:
        board = in_board

    # Launch into the key loop.
    while not board.is_checkmate() and not board.is_stalemate() and not board.is_insufficient_material() and not board.can_claim_draw() and not board.is_seventyfive_moves() and not board.is_fivefold_repetition():
        if training and sequence_no == 0:
            fen = board.fen()
            spaces_pos = [pos for pos, char in enumerate(fen) if char == ' ']
            opening_fen = fen[:spaces_pos[3]]
            
            ply_array = np.array([game_id, sequence_no, opening_fen, "", 0])
            new_row = pd.DataFrame([ply_array], columns=game_df.columns)
            game_df = pd.concat([game_df, new_row], ignore_index=True)

        sequence_no += 1
        all_moves = str(board.legal_moves)
        start_pos = [pos for pos, char in enumerate(all_moves) if char == '(']
        end_pos = [pos for pos, char in enumerate(all_moves) if char == ')']
        all_moves_string= all_moves[start_pos[0]+1:end_pos[0]]
        all_moves_string = all_moves_string.replace(" ", "")
        all_moves_array = all_moves_string.split(',')
        # random.seed(time.time())
        random_int = random.randint(0, len(all_moves_array)-1)
        next_move = all_moves_array[random_int]
        board.push_san(next_move)

        if training:
            fen = board.fen()
            spaces_pos = [pos for pos, char in enumerate(fen) if char == ' ']
            trimmed_fen = fen[:spaces_pos[3]]
            

            ply_array = np.array([game_id, sequence_no, trimmed_fen, next_move, 0])
            new_row = pd.DataFrame([ply_array], columns=game_df.columns)
            game_df = pd.concat([game_df, new_row], ignore_index=True)

    if board.is_checkmate():
        if board.outcome().winner:
            reward = 1
        else:
            reward = -1
    
    reward_array = np.full(sequence_no+1, reward)
    game_df['reward'] = reward_array

    return game_df, reward

def append_batch(games, batch_size):
    num_games = 10000    # DISTINCT FEN STATES BEFORE: 31 549 926

    batch_counter = 0
    default_reward = 0
    start_time = time.time()

    # Set the game_id by looking up the last used game_id.
    game_id_cursor = execute_sql("SELECT MAX(game_id) FROM " + replay_buffer_table +";")
    in_game_id = int(game_id_cursor.fetchall()[0][0]) + 1  # There has to be a better way to do this.

    for counter in range(num_games):
        batch_counter += 1
        out_replay_buffer_df, out_reward = play_game(None, in_game_id, training=True)
        print("Reward for game " + str(in_game_id) + " was " + str(out_reward) + ".")
    
        # Increment the game_id
        in_game_id += 1

        # Append the game dataframe to the batch dataframe.
        batch_df = pd.concat([batch_df, out_replay_buffer_df], ignore_index=True)
        
        if batch_counter == batch_size or counter == num_games-1:
            
            # Load the batch to the database.
            fastload(df = batch_df, table_name = replay_buffer_staging_table, if_exists = 'append')
            
            # Empty the batch dataframe.
            batch_df = pd.DataFrame({
                'game_id': [],
                'ply': [],
                'FEN': [],
                'move': [],
                'reward': [],
            })
            
            # Reset the batch counter.
            batch_counter = 0
            end_time = time.time()
            batch_duration = end_time-start_time
            print(str(counter+1) + " of " + str(num_games) + " completed. Last batch duration was " + str(batch_duration) + " with average game duration of " + str(batch_duration/batch_size) + ".")
            start_time = time.time()