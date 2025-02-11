"""Roulette emulation."""

import numpy as np

class Roulette():
    """European Roulette class."""

    def __init__(self):
        """The class object init parameters."""
        self.low_number = 0
        self.max_number = 37  # 0, 1-36
        # Create numbers array
        self.numbers = np.arange(self.low_number, self.max_number)

        # Create colors array for each number
        self.colors = np.zeros_like(self.numbers, dtype='U5')
        self.colors[self.numbers % 2 == 1] = 'red'
        self.colors[self.numbers % 2 == 0] = 'black'
        self.colors[self.numbers == 0] = 'green'

    def get_nums_colors(self, rnd_nums):
        """Returns color for each number."""
        return np.array(self.colors[rnd_nums])

    def spin(self, iters=1):
        """Emulates roulette spins iters times."""
        return np.random.randint(self.low_number, self.max_number, iters)


class RouletteBet():
    """Roulette Bet"""

    def __init__(self, r_obj):
        """The class object init parameters."""
        self.low_number = r_obj.low_number
        self.max_number = r_obj.max_number

    def random_bet_num(self, iters=1):
        """Simulates random roulette bet iters times."""
        return np.random.randint(self.low_number, self.max_number, iters)

    def fixed_bet_num(self, fixed_bet, iters=1):
        """Simulates placing a fixed bet iters times."""
        return np.full(iters, fixed_bet)

    def generate_bet_size(self, min_bet=1, max_bet=10, iters=1):
        """Simulates random roulette bet iters times."""
        return  np.full(iters, min_bet) if min_bet == max_bet else \
                np.random.randint(min_bet, max_bet, iters)


class BetStrategy():
    """Roulette Bet Strategy simulation class."""

    def __init__(self):
        """Init object."""
        self.roulette = Roulette()
        self.bet = RouletteBet(self.roulette)

    @staticmethod
    def compare_results(roulette_result, rand_bet_result):
        """Returns arras elements compare results."""
        return np.unique(roulette_result == rand_bet_result, return_counts=True)

    @staticmethod
    def get_probability(exp_results):
        """ Returns win probability.
            @exp_results format:  (array([False,  True]), array([lose_rate, win_rate]))"""
        probability = 0
        if len(exp_results) == 2 and len(exp_results[0]) == 2:
            iters = exp_results[1][0] + exp_results[1][1]
            probability = exp_results[1][1]/iters
        return probability

    def random_bet_and_spin(self, iters):
        """Random numbers bet strategy."""
        roulette_result = self.roulette.spin(iters)
        bet_result = self.bet.random_bet_num(iters)
        results = BetStrategy.compare_results(roulette_result, bet_result)
        return results

    def fixed_bet_and_spin(self, fixed_num, iters):
        """Random numbers bet strategy."""
        roulette_result = self.roulette.spin(iters)
        results = BetStrategy.compare_results(roulette_result, fixed_num)
        return results

    def straight_up_strategy(self, min_bet, max_bet, iters):
        """Simple Bet strategy: one number, random bet size."""
        koef = 35   # simple startegy koef = 1/35
        theor_win_prb = 0.027
        # place the bets and spin the wheel ------------------------------------------------
        roulette_result = self.roulette.spin(iters)
        bet_result = self.bet.random_bet_num(iters)
        bet_sizes = self.bet.generate_bet_size(min_bet, max_bet, iters)
        # Calculate win probability --------------------------------------------------------
        exp_results = BetStrategy.compare_results(roulette_result, bet_result)
        exp_win_prb = BetStrategy.get_probability(exp_results)
        print(f"Theoretical win: {theor_win_prb}; Experimental win: {exp_win_prb}")
        # Calculate total WIN/LOSE ---------------------------------------------------------
        win_results = np.zeros_like(roulette_result)
        win_results[roulette_result == bet_result] = bet_sizes[roulette_result == bet_result]
        total_bet = np.sum(bet_sizes)
        total_win = np.sum(win_results) * koef
        total_result = total_win - total_bet
        print(f"Total bet: {total_bet}; Win: {total_win}; Result: {total_result}")
        return total_result


if __name__ == "__main__":

    bs = BetStrategy()
    ITERS = 200000
    # simple scenarios --------------------------------------------------------------------
    rnd_res = bs.random_bet_and_spin(ITERS)
    fix_res = bs.fixed_bet_and_spin(17, ITERS)
    print(f"Random bet: {BetStrategy.get_probability(rnd_res)}")
    print(f"Fixed bet:  {BetStrategy.get_probability(fix_res)}\n")
    # custom bet scenario -----------------------------------------------------------------
    win_result = bs.straight_up_strategy(min_bet=1, max_bet=5, iters=ITERS)
