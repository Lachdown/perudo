import numpy as np

class Player(object):

    def __init__(self, name, dice, sim, char = None):
        
        if sim:
            self.update_condition = char
        self.name = name 
        self.bets = []
        self.dice_rem = dice
        self.sim = sim
    
    def roll_dice(self):

        self.dice = np.bincount(np.random.randint(0,6,(self.dice_rem,)), minlength=6)
    
    def expected_dice(self, dice_nums):

        expected_total = np.multiply(self.dice_belief.T, dice_nums)
        return np.sum(expected_total, axis=1)

    def update_expectations(self, dice_nums, bet, pl_ind):

        exp_dice = self.expected_dice(dice_nums)

        bid_ratio = bet[0] / (exp_dice[bet[1]-1] + exp_dice[0])

        delta = self.update_condition * bid_ratio

        pl_line = self.dice_belief[pl_ind, 1:]

        pl_line[bet[1]-2] += delta * 5/4

        pl_line = np.subtract(pl_line, delta/4)

        pl_line[pl_line < 0] = 0
        pl_line[pl_line > 5/6] = 5/6

        pl_line = pl_line / (np.sum(pl_line) + 1/6)

        self.dice_belief[pl_ind, 1:] = pl_line

    def reset_expectations(self, n_players, ind):

        self.dice_belief = np.array([[1/6 for i in range(6)] if i != ind else [0 for i in range(6)] for i in range(n_players)])

    def make_decision(self, prev_bet, dice_nums, perlifico):

        # calc chance of having the numbers

        exp_dice = self.expected_dice(dice_nums)

        # if expected num dice < bet

        exp_diff_prev = exp_dice[prev_bet[1]-1] + exp_dice[0] - prev_bet[0]

        if exp_diff_prev < 0:
            return 'bull'

        poss_nums = [i for i in range(2,7)]
        poss_size = np.array([prev_bet[0] if i > prev_bet[1] else prev_bet[0] + 1 for i in poss_nums])

        ones = np.array([exp_dice[0] + self.dice[0] for i in poss_nums])

        exp_diff = np.sum((exp_dice[1:], ones, -1*poss_size, self.dice[1:]), axis=0)

        if (exp_diff>0).sum() == 0:
            return 'bull'

        # select bet by weighting by expected num dice

        exp_diff[exp_diff<0] = 0
        exp_diff = exp_diff / np.sum(exp_diff)

        bet_ind = np.random.choice(5, p = exp_diff)

        return poss_size[bet_ind], poss_nums[bet_ind]

    def play_perlifico(self):
        
        print(f"Hi {self.name}!")
        print("Play Perlifico Rules (y/n):")
        x = str(input())

        return (x == 'y')

    def retrieve_bet(self, bet, perlifico):

        print(f"{self.name} turn. Current bet is {bet[0]} {bet[1]}\'s")
        print("Bullshit?? (y/n)")
        x = str(input())
        if x == 'y':
            return "bull"
        elif perlifico:
            return [bet[0]+1, bet[1]]
        else:
            bet = [0,0]
            print("Enter Dice Volume:")
            bet[0] = int(input())
            print("Enter Dice Value:")
            bet[1] = int(input())
            return bet

    def input_dice(self):

        print("Input dice (Separated by space)")
        x = str(input()).split(' ')
        self.dice = np.bincount(np.array(x, dtype=int)-1 , minlength=6)

            

        

        



