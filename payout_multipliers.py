from fractions import Fraction
from pulp import *


# Linear program to calculate the payout coefficients based on currently set reel states
# coefficients calculated against an arbitrary target payout %

rtp_target = 0.90


def machine_coefficients(symbols, absolute_probability):

    lp = LpProblem("Machine_coefficients", LpMaximize)

    decision_vars = []

    # define variables
    for symbol in symbols:
        decision_vars.append(LpVariable(symbol, 0))

    # define objective function
    objective_function = lpSum([decision_vars[i] for i in range(len(symbols))])
    lp += objective_function

    # define constraints
    lp += lpSum([decision_vars[i] * absolute_probability[symbols[i]] for i in range(len(symbols))]) <= rtp_target

    # payout multiplier must be at least 0.1 for each symbol
    for i in range(len(symbols)):
        lp += decision_vars[i] >= 0.9

    # payout multiplier must be at least 1.1x the previous symbol's payout multiplier
    for i in range(1, len(symbols)):
        lp += decision_vars[i] >= decision_vars[i - 1] * 1.3

    lp.solve()
    print("Payout Multipliers:")
    print_results(lp)
    print("Calculated RTP:")
    print(lpSum([decision_vars[i] * absolute_probability[symbols[i]] for i in range(len(symbols))]).value())
    return {symbols[i]: decision_vars[i].varValue for i in range(len(symbols))}


# print results of payout multiplier optimisation
def print_results(problem):
    sense = "min" if problem.sense == 1 else "max"
    print(f"status: {LpStatus[problem.status]}")

    for v in problem.variables():
        print(f"{v.name} = {str(Fraction(v.varValue).limit_denominator())}")

    print(f"{sense}(z) = {str(Fraction(value(problem.objective)).limit_denominator())}")

