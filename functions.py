import numpy as np
import json

def get_probability(r_A: int, r_B: int) -> tuple:
    p_A = np.round(1 / (1 + 10 ** ((r_B - r_A) / 400)),3)
    p_B = 1 - p_A
    return p_A, p_B


def get_new_rating(r: int, s: int, p: float, K: int) -> int:
    return int(np.round((r + K * (s - p)),0))

def get_new_elo(dict_elo: dict, player1: str, player2: str, s: int = 1, K: int = 32) -> dict:
    
    r_A = next((player['rating'] for player in dict_elo['players'] if player['name'] == player1), None)
    r_B = next((player['rating'] for player in dict_elo['players'] if player['name'] == player2), None)

    #r_A = dict_elo[player1]
    #r_B = dict_elo[player2]

    p_A, p_B = get_probability(r_A, r_B)

    r_A_new = get_new_rating(r_A, s, p_A, K)
    r_B_new = get_new_rating(r_B, 1 - s, p_B, K)

    # aggiorna il rating

    for player in dict_elo['players']:
        if player['name'] == player1:
            player['rating'] = r_A_new
            player['games'] += 1
            player['wins'] += 1 if s == 1 else 0
            player['losses'] += 1 if s == 0 else 0
        if player['name'] == player2:
            player['rating'] = r_B_new
            player['games'] += 1
            player['wins'] += 1 if s == 0 else 0
            player['losses'] += 1 if s == 1 else 0

    #dict_elo[player1] = r_A_new
    #dict_elo[player2] = r_B_new

    return dict_elo




def get_match_result(r_A: int, r_B: int, s: int = 1, K: int = 32) -> tuple:
    p_A, p_B = get_probability(r_A, r_B)

    print("se A vince/perde: +",K * (1 - p_A),"/ -", K * (1 - p_B))
    print("se B vince/perde: +",K * (1 - p_B),"/ -", K * (1 - p_A))

    r_A_new = get_new_rating(r_A, s, p_A, K)
    r_B_new = get_new_rating(r_B, 1 - s, p_B, K)

    return r_A_new, r_B_new