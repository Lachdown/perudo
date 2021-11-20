import numpy as np
from sim_players import Player

DICE = 5
OPT = 0.2

class Perudo(object):

    def __init__(self, character, sim = True):

        self.n_players = len(character)
        self.players = []
        self.sim = sim

        for i, crt in enumerate(character):
            if sim:
                self.players.append(Player("Player_"+str(i), DICE, True, crt))
            else:
                if i == 0:
                    self.players.append(Player(crt, DICE, True, OPT))
                else:
                    self.players.append(Player(crt, DICE, False))

        self.players = np.array(self.players)


    def run_game(self, start = 0):

        init_order = np.arange(self.n_players)
        startRound = True
        perlifico = False

        while True:
            if startRound:
                
                dice_nums = np.array([pyer.dice_rem for pyer in self.players])
                order = init_order[dice_nums>0]
                pl_order = np.concatenate((order[start:], order[:start]))
                player_order = self.players[pl_order]

                if (dice_nums>0).sum() < 2:
                    break

                for i, pl in enumerate(self.players):
                    if pl.sim:
                        pl.reset_expectations(self.n_players, i)
                    if self.sim:
                        pl.roll_dice()
                    elif i == 0:
                        pl.input_dice()
                    pl.bets.append([])
                
                bet = [0, 6]
                startRound = False

            for i, player in enumerate(player_order):
                
                if player.sim:
                    bet = player.make_decision(bet, dice_nums, perlifico)
                    if not self.sim:
                        print(f'{bet[0]} {bet[1]}\'s')
                else:
                    bet = player.retrieve_bet(bet, perlifico)
                    
                player.bets[-1].append(bet)

                if bet == 'bull':
                    
                    last_bet = player_order[i-1].bets[-1][-1]

                    if self.bullshit(last_bet):
                        start = i-1
                    else:
                        start = i

                    player_order[start].dice_rem += -1

                    if player_order[start].sim:
                        perlifico = (player_order[start].dice_rem == 1)
                    else:
                        perlifico = player_order[start].play_perlifico()

                    startRound = True
                    break
                    
                else:
                    for ind, pl in enumerate(self.players):
                        if pl.sim and not perlifico and ind != i and dice_nums[ind] != 0:
                            pl.update_expectations(dice_nums, bet, i)
         
                
        print(f"Winner is {player_order[0].name} with {player_order[0].dice_rem} d remaining")


    def bullshit(self, last_bet):

        if self.sim:

            all_dice = np.array([pl.dice for pl in self.players])
            all_dice = np.sum(all_dice, axis=0)
    

            return (all_dice[last_bet[1]-1] + all_dice[0] < last_bet[0])

        else:
            print(f"How many {last_bet[1]}'s")
            actual = int(input())

            return (actual < last_bet[0])

        # check for remove player

        # check for perlifico
