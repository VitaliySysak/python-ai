from faker import Faker
import pandas as pd
from bank_example import Client, ExtendedClient, Account, DepositAccount, Transaction, DepositTransaction, WithdrawalTransaction, Bank

df = pd.read_csv("./datasets/bank_transactions.csv")

df.info()

particular_df = df.head(100)

particular_df.to_csv("./datasets/first_1000_records.csv", index=False)

# Приклад використання - має бути замінений вашою імплементацією згідно завдання
bank = Bank()

# client = bank.create_client("Іван Петренко", "1234567890")

for index, row in particular_df.iterrows():
    fake = Faker()

    name = fake.name()
    transaction_id = row["TransactionID"]
    customer_id = row["CustomerID"]
    customer_dob = row["CustomerDOB"]
    gender = row["CustGender"]
    city = row["CustLocation"]

    client = bank.create_extended_client(name=name, transaction_id=transaction_id, customer_id=customer_id, customer_dob=customer_dob, cust_gender=gender, cust_location=city)
    account = bank.create_account(client, 1000)

    if client.cust_gender == "M":
        deposit_transaction = DepositTransaction(500)
        bank.execute_transaction(account, deposit_transaction)
    elif client.cust_gender == "F":
        withdrawal_transaction = WithdrawalTransaction(200)
        bank.execute_transaction(account, withdrawal_transaction)
    else:
        pass
        
print(bank.clients)
