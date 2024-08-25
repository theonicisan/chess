#from teradataml import *
import chess
import time
import random

def trim_fen(in_board):
        fen = in_board.fen()
        spaces_pos = [pos for pos, char in enumerate(fen) if char == ' ']
        trimmed_fen = fen[:spaces_pos[3]]
        
        return trimmed_fen

def get_new_game_id():
        
        # Set the game_id by looking up the last used game_id.
        game_id_cursor = execute_sql("SELECT MAX(game_id) FROM replay_buffer;")
        game_id = int(game_id_cursor.fetchall()[0][0]) + 1  # There has to be a better way to do this.
        
        return game_id

def insert_replay_buffer():
        
        game_id = get_new_game_id()
        
        return game_id