

import pandas as pd
from bank_example import Client, ExtendedClient, Account, DepositAccount, Transaction, DepositTransaction, WithdrawalTransaction, Bank

df = pd.read_csv("./datasets/bank_transactions.csv")

df.info()

particular_df = df.head(1000)

particular_df.to_csv("./datasets/first_1000_records.csv", index=False)

# Приклад використання - має бути замінений вашою імплементацією згідно завдання
bank = Bank()
# client = bank.create_client("Іван Петренко", "1234567890")
for index, row in df.iterrows():
    name = row["name"]
    phone = row["phone"]
    client_id = row["client_id"]
    birthdate = row["birthdate"]
    gender = row["gender"]
    city = row["city"]

    client = bank.create_extended_client(name, phone, client_id, birthdate, gender, city)
    account = bank.create_account(client, 1000)

    deposit_transaction = DepositTransaction(500)
    bank.execute_transaction(account, deposit_transaction)

    withdrawal_transaction = WithdrawalTransaction(200)
    bank.execute_transaction(account, withdrawal_transaction)

    print(client)
    print(account)


