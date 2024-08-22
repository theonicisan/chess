

from teradataml import *
import chess
import random
import numpy as np
import time

database_name = "val"
database_pw = "val"
database_ip = "192.168.56.1"

def initialize_database(database_name):

    # Connect with Teradata Database
    eng = create_context(database_ip, database_name, database_pw)
    init = get_connection()

    # Drop the tables if they already exist - if you want to start over with the disctionary.
    if init.dialect.has_table(connection=init, table_name="replay_buffer"):
        db_drop_table("replay_buffer")

    # Create the tables holding the training data.
    create_game_table = "create multiset table replay_buffer (game_id BIGINT, sequence INTEGER, FEN VARCHAR(100), move VARCHAR(10), reward FLOAT) PRIMARY INDEX (game_id);"
    execute_sql(create_game_table)

    #execute_sql("insert into replay_buffer (game_id) values (0);")

    return

def insert_replay_buffer(game_id, sequence_no, FEN, ply, reward):
    print("insert_replay_buffer executed")
    insert_replay_buffer = "INSERT INTO replay_buffer (game_id, sequence, FEN) VALUES (" + str(game_id) + "," + str(sequence_no) + ",'" + FEN + "','" + ply + "');"
    execute_sql(insert_replay_buffer)
    return 

def play_game(in_board, training=None):
    
    # Initialize the starting variables.
    sequence_no = 0
    reward = 0
    discount = 0.95

    board = chess.Board()
    if in_board is not None:
        board = in_board

    if training == True:
        # Connect with Teradata Database
        eng = create_context(database_ip, database_name, database_pw)
        conn = get_connection()
        
        # Set the game_id by looking up the last used game_id.
        game_id_cursor = execute_sql("SELECT MAX(game_id) FROM replay_buffer;")
        game_id = int(game_id_cursor.fetchall()[0][0]) + 1  # There has to be a better way to do this.

    # Launch into the key loop.
    while not board.is_checkmate() and not board.is_stalemate() and not board.is_insufficient_material() and not board.can_claim_draw() and not board.is_seventyfive_moves() and not board.is_fivefold_repetition():
        if training and sequence_no == 0:
            fen = board.fen()
            split_fen = fen.split(" -")
            opening_fen = split_fen[0]
            
            insert_replay_buffer = "INSERT INTO replay_buffer (game_id, sequence, FEN) VALUES (" + str(game_id) + "," + str(sequence_no) + ",'" + opening_fen + "');"
            execute_sql(insert_replay_buffer)

        sequence_no += 1
        all_moves = str(board.legal_moves)
        start_pos = [pos for pos, char in enumerate(all_moves) if char == '(']
        end_pos = [pos for pos, char in enumerate(all_moves) if char == ')']
        all_moves_string= all_moves[start_pos[0]+1:end_pos[0]]
        all_moves_string = all_moves_string.replace(" ", "")
        all_moves_array = all_moves_string.split(',')
        next_move = random.choice(all_moves_array)
        board.push_san(next_move)

        if training:
            fen = board.fen()
            split_fen = fen.split(" -")
            trimmed_fen = split_fen[0]
            
            insert_replay_buffer = "insert into replay_buffer (game_id, sequence, FEN, move) values (" + str(game_id) + "," + str(sequence_no) + ",'" + trimmed_fen + "','" + next_move + "');"
            execute_sql(insert_replay_buffer)
            if board.is_checkmate():
                if board.outcome().winner:
                    reward = 1
                else:
                    reward = -1

    print("The reward for " + str(game_id) + " is:" + str(reward) + ".")
    if reward == 0:
        Qsa = 0.
        execute_sql("UPDATE replay_buffer SET reward = " + str(Qsa) + " WHERE game_id = " + str(game_id) + ";")
    else:
        for turn in range(sequence_no+1):
            Qsa = reward*discount**(sequence_no - turn)
            try:
                execute_sql("UPDATE replay_buffer SET reward = " + str(Qsa) + " WHERE game_id = " + str(game_id) + " AND sequence = " + str(turn) + ";")
            except:
                execute_sql("UPDATE replay_buffer SET reward = 0. WHERE game_id = " + str(game_id) + " AND sequence = " + str(turn) + ";")


    return board