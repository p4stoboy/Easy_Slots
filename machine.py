from random import *
import numpy as np
from payout_multipliers import *

# slot machine properties

symbols = ["A", "B", "C", "D", "Z"]

# reels
reel1 = np.array(["A", "A", "A", "A", "B", "B", "C", "D", "Z"])
reel2 = np.array(["A", "A", "A", "A", "B", "B", "C", "C", "D", "D", "Z"])
reel3 = np.array(["A", "A", "B", "B", "C", "C", "D", "Z"])

cycle = len(reel1) * len(reel2) * len(reel3)

# independent single line chances relative to reel states (diagonal same as horizontal)
line_probability_percent = {
    symbol: (reel1 == symbol).sum() * (reel2 == symbol).sum() * (reel3 == symbol).sum() / cycle
    for symbol in symbols
}

# average spins required to hit line
line_hit_rates = {
    symbol: 1 / line_probability_percent[symbol]
    for symbol in symbols
}

# frequency of line hits out of 100 spins
line_hit_frequency_percent = {
    symbol: 100 / line_hit_rates[symbol]
    for symbol in symbols
}

# absolute probability of hitting win on given symbol per spin (used to calculate payout multipliers)
absolute_probability = {
    symbol: 1 - ((1 - line_probability_percent[symbol])**5)
    for symbol in symbols
}

# payout multipliers via linear optimisation
payout_multipliers = machine_coefficients(symbols, absolute_probability)

print("Line probability: ", line_probability_percent)
print("Line hit rates: ", line_hit_rates)
print("Line hit frequency: ", line_hit_frequency_percent)
print("Absolute probability: ", absolute_probability)


def spin(bet=1):
    # virtual reel implementation (much harder to constrain around rtp target)
    # -------------------------------
    # r1_start = randint(0, len(reel1))
    # r2_start = randint(0, len(reel2))
    # r3_start = randint(0, len(reel3))
    #
    # indices = [range(r1_start, r1_start+3), range(r2_start, r2_start+3), range(r3_start, r3_start+3)]
    #
    # board_state = np.array([reel1.take(indices[0], mode="wrap"), reel2.take(indices[1], mode="wrap"), reel3.take(indices[2], mode="wrap")]).transpose()
    # print(board_state)
    # -------------------------------

    # random reel implementation
    board_state = np.array([[choice(reel1) for _ in range(3)], [choice(reel2) for _ in range(3)], [choice(reel3) for _ in range(3)]]).transpose()
    # print(board_state)

    # check for line hits
    wins = hits(board_state)
    # calculate payout
    payout = sum([bet * payout_multipliers[win] for win in wins])

    return payout



def hits(board):

    hit_symbols = []
    # check every line (horiztonal, diagonal = 5 lines)
    for i in range(3):
        # horizontal
        if board[i][0] == board[i][1] == board[i][2]:
            hit_symbols.append(board[i][0])
    # diagonal
    if board[0][0] == board[1][1] == board[2][2]:
        hit_symbols.append(board[0][0])
    if board[0][2] == board[1][1] == board[2][0]:
        hit_symbols.append(board[0][2])
    return hit_symbols
