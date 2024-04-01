### Bank Management System

This Python program implements a simple bank management system with classes representing clients, accounts, transactions, and transaction history.

### Usage

To use this system, you can follow the example below:

```python
# Import necessary classes
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

# Define your clients and accounts
class Client:
    # Implementation

class IndividualClient(Client):
    # Implementation

class Account:
    # Implementation

class CheckingAccount(Account):
    # Implementation

class History:
    # Implementation

class Transaction(ABC):
    # Implementation

class Withdrawal(Transaction):
    # Implementation

class Deposit(Transaction):
    # Implementation

# Example usage
if __name__ == "__main__":
    # Create clients
    client1 = IndividualClient("John", datetime(1990, 5, 15), "123.456.789-00", "Street A, 123")
    client2 = IndividualClient("Mary", datetime(1985, 10, 25), "987.654.321-00", "Street B, 456")

    # Create accounts
    account1 = CheckingAccount.new_account(client1, "12345")
    account2 = CheckingAccount.new_account(client2, "54321")

    # Perform transactions
    withdrawal = Withdrawal(1000)
    withdrawal.register(account1)

    deposit = Deposit(500)
    deposit.register(account2)
```

### Classes

1. **Client**: Represents a client with an address and accounts.
2. **IndividualClient**: Represents a physical person, inherits from Client.
3. **Account**: Represents a bank account with a balance, number, agency, client, and transaction history.
4. **CheckingAccount**: Represents a checking account, inherits from Account, with additional attributes like withdrawal limit and transaction limit.
5. **History**: Represents the transaction history associated with an account.
6. **Transaction**: Abstract base class for transactions.
7. **Withdrawal**: Represents a withdrawal transaction.
8. **Deposit**: Represents a deposit transaction.

### Contributing

Feel free to contribute to this project by forking it and submitting pull requests with your enhancements or bug fixes.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
