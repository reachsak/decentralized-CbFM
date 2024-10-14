from brownie import MoralisGovernor, accounts,TimeLock

def main():
    # Load the Timelock contract
    governor = TimeLock[-1]  # Assuming the last deployed instance of MoralisGovernor
    print(governor)

    # Get the balance of the contract
    balance = governor.balance()
    
    # Print the DAO address and balance
    print(f"DAO Address: {governor}")
    print(f"DAO Balance: {balance}")