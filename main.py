from game import Perudo
import numpy as np

if __name__ == "__main__":

    char = ["Lachlan"] + ['PLAYER_'+str(i+1) for i in range(5)]
    game = Perudo(char, sim  = False)

    game.run_game(0)

