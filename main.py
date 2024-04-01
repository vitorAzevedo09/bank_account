from datetime import datetime

# Client functions
def create_client(address):
    return {"address": address, "accounts": []}

def add_account_to_client(client, account):
    client["accounts"].append(account)

# Individual client functions
def create_individual_client(name, date_of_birth, cpf, address):
    return {"name": name, "date_of_birth": date_of_birth, "cpf": cpf, **create_client(address)}

# Account functions
def create_account(number, client):
    return {"number": number, "client": client, "balance": 0, "branch": "0001", "history": []}

def deposit(account, amount):
    if amount > 0:
        account["balance"] += amount
        account["history"].append(("Deposit", amount, datetime.now()))
        print("\n=== Deposit successful! ===")
    else:
        print("\n@@@ Operation failed! The entered amount is invalid. @@@")
    return account

def withdraw(account, amount):
    balance = account["balance"]
    exceeded_balance = amount > balance

    if exceeded_balance:
        print("\n@@@ Operation failed! You do not have enough balance. @@@")
    elif amount > 0:
        account["balance"] -= amount
        account["history"].append(("Withdrawal", amount, datetime.now()))
        print("\n=== Withdrawal successful! ===")
    else:
        print("\n@@@ Operation failed! The entered amount is invalid. @@@")
    return account

# History functions
def add_transaction_to_history(account, transaction_type, amount, date):
    account["history"].append((transaction_type, amount, date))
    return account

# Main menu functions
def main_menu():
    print("\nMain Menu:")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. View Account Details")
    print("4. View History Transactions")
    print("5. Exit")

def deposit_menu():
    amount = float(input("Enter the deposit amount: "))
    return amount

def withdraw_menu():
    amount = float(input("Enter the withdrawal amount: "))
    return amount

def view_account_details(account):
    print("\nAccount Details:")
    print(f"Branch:\t{account['branch']}")
    print(f"Account:\t{account['number']}")
    print(f"Holder:\t{account['client']['name']}")

def view_history_transactions(account):
    print("\nHistory Transactions:")
    for transaction in account["history"]:
        print(f"Type: {transaction[0]}, Amount: {transaction[1]}, Date: {transaction[2]}")

def run_bank_management_system():
    client = create_individual_client("John Doe", "1990-01-01", "123456789", "123 Main St")
    account = create_account("123456", client)

    while True:
        main_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            amount = deposit_menu()
            account = deposit(account, amount)

        elif choice == "2":
            amount = withdraw_menu()
            account = withdraw(account, amount)

        elif choice == "3":
            view_account_details(account)

        elif choice == "4":
            view_history_transactions(account)

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    run_bank_management_system()
