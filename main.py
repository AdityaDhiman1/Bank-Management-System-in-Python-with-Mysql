import mysql.connector
from datetime import datetime


class Bank:
    def __init__(self, account_number, name, balance, transaction_date=None):
        self.account_number = account_number
        self.name = name
        self.balance = balance
        self.transaction_date = transaction_date

    def deposit(self, amount):
        self.balance = self.balance + amount
        self.transaction_date = datetime.now()

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance = self.balance - amount
        self.transaction_date = datetime.now()

    def check_balance(self):
        return self.balance

#This class create database and update
class BankDatabase:
    def __init__(self):
        self.database = mysql.connector.connect(host='localhost', user='root', password='', database='BANK')
        self.cur = self.database.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
               CREATE TABLE IF NOT EXISTS accounts (
                 account_number INT PRIMARY KEY,
                 name VARCHAR(255),
                 balance FLOAT,
                 transaction_date TIMESTAMP
               );
           """)
        self.database.commit()

    def create_account(self, account_number, name, balance, transaction_date=None):
        query = "insert into accounts (account_number,name,balance,transaction_date) values(%s, %s, %s, %s)"
        values = (account_number, name, balance, transaction_date)
        self.cur.execute(query, values)
        self.database.commit()

    def get_account(self, account_number):
        query = "select account_number, name, balance, transaction_date from accounts where account_number = %s"
        values = (account_number,)
        self.cur.execute(query, values)
        result = self.cur.fetchone()
        if not result:
            return None
        account_number, name, balance, transaction_date = result
        return Bank(account_number, name, balance, transaction_date)

    def update_account(self, account_number, balance, transaction_date=None):
        query = "update accounts set balance = %s, transaction_date = %s where account_number = %s"
        values = (balance, transaction_date, account_number)
        self.cur.execute(query, values)
        self.database.commit()


def main():
    db = BankDatabase()

    while True:
        print("1. Create Account")
        print("2. Deposit money")
        print("3. Withdraw money ")
        print("4. check balance")
        print("5. Transfer")
        print("6. Exit")

        try:
            ch = int(input("Enter your choice (1-6):"))
        except ValueError:
            print("invalid choice")
            continue

        if ch == 1:
            account_number = input("Enter account number : ")
            name = input("Enter name : ")
            balance = float(input("Enter balance : "))
            transaction_date = datetime.now()
            db.create_account(account_number, name, balance, transaction_date)
            print("Account created successfully")
        elif ch == 2:
            account_number = input("Enter account number : ")
            account = db.get_account(account_number)
            if account:
                amount = float(input("Enter amount deposit:"))
                account.deposit(amount)
                db.update_account(account_number, account.check_balance(), account.transaction_date)
                print("Amount deposit successfully")
            else:
                print("Account not found")
        elif ch == 3:
            account_number = input("Enter account number :")
            account = db.get_account(account_number)
            if account:
                amount = float(input("Enter amount to withdraw :"))
                try:
                    account.withdraw(amount)
                    db.update_account(account_number, account.check_balance(), account.transaction_date)
                    print("Amount withdrawn successfully")
                except ValueError as e:
                    print(str(e))
            else:
                print("Account not found")
        elif ch == 4:
            account_number = input("Enter account number :")
            account = db.get_account(account_number)
            if account:
                print("Name :", account.name)
                print("Balance :", account.check_balance())
                print("Transaction date :", account.transaction_date)
            else:
                print("Account not found")
        elif ch == 5:
            account_number = input("Enter account number from which you want to transfer :")
            account1 = db.get_account(account_number)
            if account1:
                account_number = input("Enter account number to which you want to transfer :")
                account2 = db.get_account(account_number)
                if account2:
                    amount = float(input("Enter amount to transfer :"))
                    try:
                        account1.withdraw(amount)
                        account2.deposit(amount)
                        db.update_account(account1.account_number, account1.check_balance(), account1.transaction_date)
                        db.update_account(account2.account_number, account2.check_balance(), account2.transaction_date)
                        print("Amount transferred successfully")
                    except ValueError as e:
                        print(str(e))
                else:
                    print("Account not found")
            else:
                print("Account not found")
        elif ch == 6:
            break
        else:
            print("Invalid choice")
if __name__ == "__main__":
    main()
