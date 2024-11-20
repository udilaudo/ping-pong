import json
import matplotlib.pyplot as plt
import argparse
import pandas as pd

from functions import *

def update_data(player1: str = "Umberto", player2: str = "Paolo", score: int = 1):

    # Load the data
    with open('players.json') as f:
        data = json.load(f)

    # Aggiorna l'elo
    get_new_elo(data, player1, player2, score)

    print(f"{player1} vs {player2}\nVittoria di {player1}\nElo aggiornati:\n{player1}: {data['players'][0]['rating']}\n{player2}: {data['players'][1]['rating']}")

    # sorta il dizionario
    data['players'] = sorted(data['players'], key=lambda x: x['rating'], reverse=True)

    # Save the data
    with open('players.json', 'w') as f:
        json.dump(data, f, indent=4)

    # crea dataframe
    df = pd.DataFrame(data["players"])

    # aggiungi una colonna win rate al dataframe arrotondata al secondo decimale
    df['win_rate'] = (df['wins'] / df['games']).round(2)

    # salva il dataframe
    df.to_csv('./results/rating.csv', index=False)

    # Plotta gli elo
    plt.figure(figsize=(15,10))
    plt.bar(df['name'], df['rating'], color='skyblue')
    plt.xticks(rotation=45)
    plt.ylabel('Rating')
    plt.title('Elo rating')
    plt.savefig('./plots/rating.png')
    plt.close()

    # Plotta le win_rate
    plt.figure(figsize=(15,10))
    plt.bar(df['name'], df['win_rate'], color='skyblue')
    plt.xticks(rotation=45)
    plt.ylabel('Win rate')
    plt.title('Win rate')
    plt.savefig('./plots/win_rate.png')
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("player1", nargs='?', help="Nome del primo giocatore", default="Umberto")
    parser.add_argument("player2", nargs='?', help="Nome del secondo giocatore", default="Paolo")
    parser.add_argument("-s", "--score", help="Risultato della partita", type=int, default=1)

    # Parse the arguments
    args = parser.parse_args()


    update_data(args.player1, args.player2, args.score)