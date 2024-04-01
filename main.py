from abc import ABC, abstractmethod
from datetime import datetime

class Client:
    """
    Represents a client.
    """

    def __init__(self, address):
        """
        Initialize a client with an address and an empty list of accounts.
        """
        self.address = address
        self.accounts = []

    def perform_transaction(self, account, transaction):
        """
        Perform a transaction on a given account.

        Parameters:
        - account: Account object on which the transaction will be performed.
        - transaction: Transaction object representing the transaction to be performed.
        """
        transaction.register(account)

    def add_account(self, account):
        """
        Add an account to the client's list of accounts.

        Parameters:
        - account: Account object to be added.
        """
        self.accounts.append(account)

class Individual(Client):
    """
    Represents an individual client.
    """

    def __init__(self, name, date_of_birth, cpf, address):
        """
        Initialize an individual client with a name, date of birth, CPF, and address.

        Parameters:
        - name: Name of the individual.
        - date_of_birth: Date of birth of the individual.
        - cpf: CPF (Cadastro de Pessoas Físicas) of the individual.
        - address: Address of the individual.
        """
        super().__init__(address)
        self.name = name
        self.date_of_birth = date_of_birth
        self.cpf = cpf

class Account:
    """
    Represents a bank account.
    """

    def __init__(self, number, client):
        """
        Initialize an account with a number, client, zero balance, branch number, and empty history.

        Parameters:
        - number: Account number.
        - client: Client object associated with the account.
        """
        self._balance = 0
        self._number = number
        self._branch = "0001"
        self._client = client
        self._history = History()

    @classmethod
    def new_account(cls, client, number):
        """
        Create a new account for a given client.

        Parameters:
        - client: Client object to which the account will belong.
        - number: Account number.

        Returns:
        - Account object.
        """
        return cls(number, client)

    @property
    def balance(self):
        """
        Get the current balance of the account.

        Returns:
        - Current balance.
        """
        return self._balance

    @property
    def number(self):
        """
        Get the account number.

        Returns:
        - Account number.
        """
        return self._number

    @property
    def branch(self):
        """
        Get the branch number of the account.

        Returns:
        - Branch number.
        """
        return self._branch

    @property
    def client(self):
        """
        Get the client associated with the account.

        Returns:
        - Client object.
        """
        return self._client

    @property
    def history(self):
        """
        Get the transaction history of the account.

        Returns:
        - History object containing the transaction history.
        """
        return self._history

    def withdraw(self, amount):
        """
        Withdraw a specified amount from the account.

        Parameters:
        - amount: Amount to be withdrawn.

        Returns:
        - True if the withdrawal was successful, False otherwise.
        """
        balance = self.balance
        exceeded_balance = amount > balance

        if exceeded_balance:
            print("\n@@@ Operation failed! You do not have enough balance. @@@")
        elif amount > 0:
            self._balance -= amount
            print("\n=== Withdrawal successful! ===")
            return True
        else:
            print("\n@@@ Operation failed! The entered amount is invalid. @@@")
        return False

    def deposit(self, amount):
        """
        Deposit a specified amount into the account.

        Parameters:
        - amount: Amount to be deposited.

        Returns:
        - True if the deposit was successful, False otherwise.
        """
        if amount > 0:
            self._balance += amount
            print("\n=== Deposit successful! ===")
        else:
            print("\n@@@ Operation failed! The entered amount is invalid. @@@")
            return False
        return True

class CheckingAccount(Account):
    """
    Represents a checking account.
    """

    def __init__(self, number, client, limit=500, withdrawal_limit=3):
        """
        Initialize a checking account with a number, client, limit, and withdrawal limit.

        Parameters:
        - number: Account number.
        - client: Client object associated with the account.
        - limit: Limit for each withdrawal (default is 500).
        - withdrawal_limit: Maximum number of withdrawals allowed (default is 3).
        """
        super().__init__(number, client)
        self.limit = limit
        self.withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        """
        Withdraw a specified amount from the account, taking into account the withdrawal limit.

        Parameters:
        - amount: Amount to be withdrawn.

        Returns:
        - True if the withdrawal was successful, False otherwise.
        """
        withdrawal_count = len(
            [transaction for transaction in self.history.transactions if transaction["type"] == Withdrawal.__name__]
        )

        exceeded_limit = amount > self.limit
        exceeded_withdrawals = withdrawal_count >= self.withdrawal_limit

        if exceeded_limit:
            print("\n@@@ Operation failed! The withdrawal amount exceeds the limit. @@@")
        elif exceeded_withdrawals:
            print("\n@@@ Operation failed! Maximum number of withdrawals exceeded. @@@")
        else:
            return super().withdraw(amount)
        return False

    def __str__(self):
        """
        Return a string representation of the checking account.

        Returns:
        - String representation.
        """
        return f"""\
            Branch:\t{self.branch}
            Account:\t{self.number}
            Holder:\t{self.client.name}
        """

class History:
    """
    Represents the transaction history of an account.
    """

    def __init__(self):
        """
        Initialize an empty transaction history.
        """
        self._transactions = []

    @property
    def transactions(self):
        """
        Get the list of transactions in the history.

        Returns:
        - List of transactions.
        """
        return self._transactions

    def add_transaction(self, transaction):
        """
        Add a transaction to the history.

        Parameters:
        - transaction: Transaction object to be added.
        """
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "amount": transaction.amount,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transaction(ABC):
    """
    Represents a transaction.
    """

    @property
    @abstractmethod
    def amount(self):
        """
        Get the amount involved in the transaction.

        Returns:
        - Amount of the transaction.
        """
        pass

    @abstractmethod
    def register(self, account):
        """
        Register the transaction on a given account.

        Parameters:
        - account: Account object on which the transaction will be registered.
        """
        pass

class Withdrawal(Transaction):
    """
    Represents a withdrawal transaction.
    """

    def __init__(self, amount):
        """
        Initialize a withdrawal transaction with a specified amount.

        Parameters:
        - amount: Amount to be withdrawn.
        """
        self._amount = amount

    @property
    def amount(self):
        """
        Get the amount of the withdrawal transaction.

        Returns:
        - Amount of the withdrawal.
        """
        return self._amount

    def register(self, account):
        """
        Register the withdrawal transaction on a given account.

        Parameters:
        - account: Account object on which the withdrawal transaction will be registered.
        """
        success_transaction = account.withdraw(self.amount)

        if success_transaction:
            account.history.add_transaction(self)

class Deposit(Transaction):
    """
    Represents a deposit transaction.
    """

    def __init__(self, amount):
        """
        Initialize a deposit transaction with a specified amount.

        Parameters:
        - amount: Amount to be deposited.
        """
        self._amount = amount

    @property
    def amount(self):
        """
        Get the amount of the deposit transaction.

        Returns:
        - Amount of the deposit.
        """
        return self._amount

    def register(self, account):
        """
        Register the deposit transaction on a given account.

        Parameters:
        - account: Account object on which the deposit transaction will be registered.
        """
        success_transaction = account.deposit(self.amount)

        if success_transaction:
            account.history.add_transaction(self)

def main_menu():
    """
    Display the main menu options.
    """
    print("\nMain Menu:")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. View Account Details")
    print("4. View History Transactions")
    print("5. Exit")

def deposit_menu():
    """
    Prompt the user to enter the deposit amount and return a Deposit object.
    """
    amount = float(input("Enter the deposit amount: "))
    return Deposit(amount)

def withdraw_menu():
    """
    Prompt the user to enter the withdrawal amount and return a Withdrawal object.
    """
    amount = float(input("Enter the withdrawal amount: "))
    return Withdrawal(amount)

def view_account_details(account):
    """
    Display the account details.

    Parameters:
    - account: Account object whose details will be displayed.
    """
    print("\nAccount Details:")
    print(account)

def view_history_transactions(account):
    """
    Display the transaction history of the account.

    Parameters:
    - account: Account object whose transaction history will be displayed.
    """
    print("\nHistory Transactions:")
    for transaction in account.history.transactions:
        print(f"Type: {transaction['type']}, Amount: {transaction['amount']}, Date: {transaction['date']}")

if __name__ == "__main__":
    # Creating a sample client and account
    client = Individual("John Doe", "1990-01-01", "123456789", "123 Main St")
    account = CheckingAccount("123456", client)

    while True:
        main_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            deposit_transaction = deposit_menu()
            client.perform_transaction(account, deposit_transaction)

        elif choice == "2":
            withdraw_transaction = withdraw_menu()
            client.perform_transaction(account, withdraw_transaction)

        elif choice == "3":
            view_account_details(account)

        elif choice == "4":
            view_history_transactions(account)

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
