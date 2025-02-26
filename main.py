from faker import Faker
import pandas as pd
from bank_example import DepositTransaction, WithdrawalTransaction, Bank
from bank_info import BankInfo

df = pd.read_csv("./datasets/bank_transactions.csv")

df.info()

particular_df = df.head(100)
df = particular_df.dropna()

df.to_csv("./datasets/first_1000_records.csv", index=False)

bank = Bank()

for index, row in df.iterrows():
    fake = Faker()
    name = fake.name()
    transaction_id = row["TransactionID"]
    customer_id = row["CustomerID"]
    customer_dob = row["CustomerDOB"]
    gender = row["CustGender"]
    city = row["CustLocation"]
    total_balance = row["CustAccountBalance"]

    client = bank.create_extended_client(name=name, transaction_id=transaction_id, customer_id=customer_id, customer_dob=customer_dob, cust_gender=gender, cust_location=city)
    account = bank.create_account(client, total_balance)

    if client.cust_gender == "M":
        deposit_transaction = DepositTransaction(500)
        bank.execute_transaction(account, deposit_transaction)
    elif client.cust_gender == "F":
        withdrawal_transaction = WithdrawalTransaction(200)
        bank.execute_transaction(account, withdrawal_transaction)
    else:
        pass

bank_info = BankInfo(bank, df)
print(bank_info.calculate_initial_balance())
print(bank_info.calculate_final_balance())
bank_info.compare_balances()
