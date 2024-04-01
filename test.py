import pytest
from main import  Individual, CheckingAccount, Deposit, Withdrawal

@pytest.fixture
def sample_account():
    client = Individual("John Doe", "1990-01-01", "123456789", "123 Main St")
    account = CheckingAccount("123456", client)
    return account

def test_deposit(sample_account):
    initial_balance = sample_account.balance
    deposit_amount = 100
    Deposit(deposit_amount)
    sample_account.deposit(deposit_amount)
    assert sample_account.balance == initial_balance + deposit_amount

def test_withdraw(sample_account):
    initial_balance = sample_account.balance
    withdrawal_amount = 50
    Withdrawal(withdrawal_amount)
    sample_account.withdraw(withdrawal_amount)
    assert sample_account.balance == initial_balance - withdrawal_amount

def test_withdraw_limit(sample_account):
    # Test that exceeding withdrawal limit fails
    withdrawal_amount = 100
    Withdrawal(withdrawal_amount)
    for _ in range(sample_account.withdrawal_limit):
        sample_account.withdraw(withdrawal_amount)
    assert not sample_account.withdraw(withdrawal_amount)

def test_insufficient_balance(sample_account):
    # Test that withdrawing more than balance fails
    withdrawal_amount = sample_account.balance + 1
    Withdrawal(withdrawal_amount)
    assert not sample_account.withdraw(withdrawal_amount)
