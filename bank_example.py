from abc import ABC, abstractmethod

class Client:
    def __init__(self, name, id_number):
        self.name = name
        self.id_number = id_number
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def __str__(self):
        return f"Клієнт: {self.name} (ID: {self.id_number})"
    
class ExtendedClient(Client):
    def __init__(self, name, transaction_id, customer_id, customer_dob, cust_gender, cust_location):
        super().__init__(name, transaction_id)
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.customer_dob = customer_dob
        self.cust_gender = cust_gender
        self.cust_location = cust_location

    def __str__(self):
        return (f"Клієнт: {self.name} (ID: {self.transaction_id}, CustomerID: {self.customer_id}, "
                f"Дата народження: {self.customer_dob}, Стать: {self.cust_gender}, Локація: {self.cust_location})")

class Account(ABC):
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    def __str__(self):
        return f"Рахунок №{self.account_number}: {self.balance} грн."

class DepositAccount(Account):
    def deposit(self, amount):
        self.balance += amount
        print(f"На рахунок №{self.account_number} внесено {amount} грн. Баланс: {self.balance} грн.")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"З рахунку №{self.account_number} знято {amount} грн. Баланс: {self.balance} грн.")
        else:
            print(f"Недостатньо коштів на рахунку №{self.account_number}.")

class Transaction(ABC):
    def __init__(self, amount):
        self.amount = amount

    @abstractmethod
    def execute(self, account):
        pass

class DepositTransaction(Transaction):
    def execute(self, account):
        account.deposit(self.amount)

class WithdrawalTransaction(Transaction):
    def execute(self, account):
        account.withdraw(self.amount)

class Bank:
    def __init__(self):
        self.clients = []
        self.next_account_number = 1

    def create_client(self, name, id_number):
        client = Client(name, id_number)
        self.clients.append(client)
        return client

    def create_account(self, client, balance):
        account = DepositAccount(self.next_account_number, balance)
        client.add_account(account)
        self.next_account_number += 1
        return account

    def create_extended_client(self, name, transaction_id, customer_id, customer_dob, cust_gender, cust_location):
        client = ExtendedClient(name, transaction_id, customer_id, customer_dob, cust_gender, cust_location)
        self.clients.append(client)
        return client

    def execute_transaction(self, account, transaction):
        transaction.execute(account)

    def __str__(self):
        return "Банк"

# Приклад використання - має бути замінений вашою імплементацією згідно завдання
bank = Bank()
# client = bank.create_client("Іван Петренко", "1234567890")
client = bank.create_extended_client("Іван Петренко", "1234567890", "CUST001", "1985-06-15", "Чоловік", "Київ")
account = bank.create_account(client, 1000)

deposit_transaction = DepositTransaction(500)
bank.execute_transaction(account, deposit_transaction)

withdrawal_transaction = WithdrawalTransaction(200)
bank.execute_transaction(account, withdrawal_transaction)

print(client)
print(account)
