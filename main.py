import numpy as np

"""
Використання основних методів NumPy
Основне завдання (спільне для всіх студентів):
"""

# 1. Створення масивів:
# 1.1 Створити масив розмірністю 5x5, заповнений випадковими числами від 0 до 1.
arr1 = np.random.rand(5, 5)
# 1.2 Створити масив розмірністю 10, заповнений числами від 10 до 20 з кроком 2.
arr2 = np.tile(np.arange(10, 20, 2), 2)
# 1.3 Створити матрицю розмірністю 3x3, заповнену нулями.
arr3 = np.array([
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
])
# 1.4 Створити матрицю розмірністю 4x4, заповнену одиницями.
arr4 = np.array([
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
])

# 2. Операції з масивами:
# 2.1 Знайти суму всіх елементів створеного масиву 5x5.
print(arr1.sum())
# 2.2 Знайти середнє значення елементів створеного масиву розміром 10 елементів.
print(arr2.mean())
# 2.3 Знайти максимальне та мінімальне значення елементів створеної матриці 5x5.
print(arr1.min())
print(arr1.max())
# 2.4 Помножити матрицю 4x4 на число 5.
print(arr4 * 5)
# 2.5 Виконати матричне множення двох матриць розмірністю 3x3 (створити окремо).
matrix1 = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])

matrix2 = np.array([
    [10, 11, 12],
    [13, 14, 15],
    [16, 17, 18],
])
print(np.dot(matrix1, matrix2))
# 3. Індексація та зрізи:
# 3.1 Вивести на екран елемент, що знаходиться на перетині 2-го рядка та 3-го стовпця матриці 5x5.
print(arr1[1][2])
# 3.2 Вивести на екран всі елементи 2-го стовпця матриці 4x4.
print(arr4[:, 1])
# 3.3 Вивести на екран всі елементи 1-го рядка матриці 3x3.
print(arr3[0])
# 3.4 Змінити значення елемента, що знаходиться на перетині 1-го рядка та 1-го стовпця матриці 5x5, на 10.
arr1[0][0] = 10
print(arr1)
# 4. Функції для роботи з масивами:
# 4.1 Використовуючи функцію reshape(), змінити розмірність масиву 10 на 2x5.
print(arr2.reshape(2, 5))
# 4.2 Використовуючи функцію flatten(), перетворити матрицю 4x4 на одновимірний масив.
print(arr4.flatten())
# 4.3 Використовуючи функцію concatenate(), об'єднати два масиви 10 в один масив розмірністю 20.
print(np.concatenate([arr2, arr2]))
# 5. Запис та читання масивів з файлів:
# 5.1 Зберегти створений масив 5x5 у файл з розширенням .npy.
np.save("./matrix", arr1)
# 5.2 Завантажити збережений масив з файлу та вивести його на екран.
print(np.load("matrix.npy"))

# Індивідуальне завдання.
# 6. Розробити імітаційну модель стратегії ставок в грі рулетка.
# Загальний опис об'єкту моделювання: 
# https://uk.wikipedia.org/wiki/%D0%A0%D1%83%D0%BB%D0%B5%D1%82%D0%BA%D0%B0_(%D0%B0%D0%B7%D0%B0%D1%80%D1%82%D0%BD%D0%B0_%D0%B3%D1%80%D0%B0)
# За основу потрібно взяти код реалізації гри рулетка, приєднаний до цього завдання.
# Уважно ознайомитися з імплементацією імітаційної моделі гри рулетка (в основі лежить використання python бібліотеки numpy).
# Провести моделювання для різної кількості ітерацій, фіксованої суми ставки, фіксованого номера, випадкових номерів для вибору ставки. За результатами зробити короткий висновок.
# До розробленої моделі додати свій метод імітації ігрової стратегії згідно індивідуального завдання.
# Провести імітаційне моделювання процесу гри з використанням імплементованої вами ігрової стратегії.
# Порівняти результати моделювання з очікуваним теоретичним значенням імовірності виграшу.
# При імплементації свого методу використовувати елементи бібліотеки numpy.
# Перевірити код статичним аналізатором коду на відповідність його code conventions. Коефіцієнт має бути більше 9.5.

# 7. Dozen — ставка «на дюжину». Оплата виграшу 2:1. Можливі ставки на одну із трьох дюжин: першу (номери 1-12),
# другу (номери 13-24) і третю (номери 25-36).
# Шанси на виграш: 12 проти 25. Імовірність: 0,324.
# Фішка ставиться поле з позначенням вибраної дюжини. При випаданні на рулетці zero, ставки на дюжини програють.


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
    
    def dozen_bet_and_spin(self, chosen_dozen, min_bet, max_bet, iters):
        """Simulates betting on a dozen (1-12, 13-24, 25-36)."""
        payout_ratio = 2 
        theoretical_win_prob = 12 / 37 

        roulette_result = self.roulette.spin(iters)
        bet_sizes = self.bet.generate_bet_size(min_bet, max_bet, iters)

        if chosen_dozen == 1:
            win_condition = (roulette_result >= 1) & (roulette_result <= 12)
        elif chosen_dozen == 2:
            win_condition = (roulette_result >= 13) & (roulette_result <= 24)
        elif chosen_dozen == 3:
            win_condition = (roulette_result >= 25) & (roulette_result <= 36)
        else:
            raise ValueError("Invalid dozen selection. Choose 1, 2, or 3.")

        exp_results = np.unique(win_condition, return_counts=True)
        exp_win_prob = self.get_probability(exp_results)
        print(f"Theoretical win: {round(theoretical_win_prob, 3)}; Experimental win: {round(exp_win_prob, 3)}")

        win_results = np.zeros_like(roulette_result)
        win_results[win_condition] = bet_sizes[win_condition] * payout_ratio
        total_bet = np.sum(bet_sizes)
        total_win = np.sum(win_results)
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

    # 7. Dozen — ставка «на дюжину». Оплата виграшу 2:1. Можливі ставки на одну із трьох дюжин: першу (номери 1-12),
    # другу (номери 13-24) і третю (номери 25-36).
    # Шанси на виграш: 12 проти 25. Імовірність: 0,324.
    # Фішка ставиться поле з позначенням вибраної дюжини. При випаданні на рулетці zero, ставки на дюжини програють.

    chosen_dozen = 2  # Betting on the second dozen (13-24)
    print("Dozen Bet Scenario")
    bs.dozen_bet_and_spin(chosen_dozen, min_bet=1, max_bet=5, iters=ITERS)

