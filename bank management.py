import sqlite3
import datetime

# Connect to database
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_number TEXT PRIMARY KEY,
    pin TEXT,
    balance REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    account_number TEXT,
    details TEXT
)
""")
conn.commit()


# Create Account
def create_account(acc_no, pin):
    cursor.execute("SELECT * FROM accounts WHERE account_number=?", (acc_no,))
    if cursor.fetchone():
        print("Account already exists")
    else:
        cursor.execute("INSERT INTO accounts VALUES (?, ?, ?)", (acc_no, pin, 0))
        conn.commit()
        print("Account Created Successfully")


# Login
def login(acc_no, pin):
    cursor.execute("SELECT * FROM accounts WHERE account_number=? AND pin=?", (acc_no, pin))
    return cursor.fetchone()


# Credit
def credit(acc_no, amount):
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_number=?", (amount, acc_no))
    cursor.execute("INSERT INTO transactions VALUES (?, ?)",
                   (acc_no, f"{datetime.datetime.now()} - Credited {amount}"))
    conn.commit()
    print("Amount Credited")


# Debit
def debit(acc_no, amount):
    cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (acc_no,))
    balance = cursor.fetchone()[0]

    if amount <= balance:
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_number=?", (amount, acc_no))
        cursor.execute("INSERT INTO transactions VALUES (?, ?)",
                       (acc_no, f"{datetime.datetime.now()} - Debited {amount}"))
        conn.commit()
        print("Amount Debited")
    else:
        print("Insufficient Balance")


# Show Balance
def show_balance(acc_no):
    cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (acc_no,))
    print("Current Balance:", cursor.fetchone()[0])


# Show Transactions
def show_transactions(acc_no):
    cursor.execute("SELECT details FROM transactions WHERE account_number=?", (acc_no,))
    for row in cursor.fetchall():
        print(row[0])


# -------- MENU --------

while True:
    print("\n1.Create Account\n2.Login\n3.Exit")
    choice = input("Enter choice: ")

    if choice == "1":
        acc = input("Enter Account Number: ")
        pin = input("Set PIN: ")
        create_account(acc, pin)

    elif choice == "2":
        acc = input("Enter Account Number: ")
        pin = input("Enter PIN: ")

        if login(acc, pin):
            print("Login Successful")
            while True:
                print("\n1.Credit\n2.Debit\n3.Balance\n4.Transactions\n5.Logout")
                ch = input("Enter choice: ")

                if ch == "1":
                    amt = float(input("Enter Amount: "))
                    credit(acc, amt)

                elif ch == "2":
                    amt = float(input("Enter Amount: "))
                    debit(acc, amt)

                elif ch == "3":
                    show_balance(acc)

                elif ch == "4":
                    show_transactions(acc)

                elif ch == "5":
                    break
        else:
            print("Invalid Account or PIN")

    elif choice == "3":
        break