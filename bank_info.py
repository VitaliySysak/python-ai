class BankInfo:
    def __init__(self, bank, df):
        self.bank = bank
        self.df = df

    def calculate_initial_balance(self):
        return self.df["CustAccountBalance"].sum()

    def calculate_final_balance(self):
        total = 0
        for client in self.bank.clients:
            for account in client.accounts:
                total += account.balance
        return total

    def compare_balances(self):
        initial_balance = self.calculate_initial_balance()
        final_balance = self.calculate_final_balance()
        difference = final_balance - initial_balance
        
        print(f"Початковий загальний баланс: {initial_balance}")
        print(f"Фінальний загальний баланс: {final_balance}")
        print(f"Різниця після транзакцій: {difference}")
        
        if difference > 0:
            print("Кошти збільшилися внаслідок депозитів.")
        elif difference < 0:
            print("Кошти зменшилися внаслідок зняття коштів.")
        else:
            print("Загальний баланс не змінився.")
