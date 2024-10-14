# scripts/transfer_eth.py
from brownie import Timelock, accounts
from scripts.helpful_scripts import get_account
def main():
    # Replace these with the actual values for your setup
    timelock_address = "0xF818E2afC78E92f526B3478832e1613e8231952A"  # Address of the deployed Timelock contract
    external_contract_address = "0xC9602ab8682443e3e0391Aa9b86E0360479B85C2"  # Address of the external contract
    amount_to_transfer = "0.02 ether"  # Amount of ETH to transfer

    # Connect to the deployed Timelock contract
    timelock = Timelock.at(timelock_address)

    # Get the address of the account proposing the transaction
    proposer = accounts.load("your_account")

    # Propose the transaction
    timelock.proposePeriod(timelock.delay())  # Check the delay period
    tx = timelock.queueTransaction(
        external_contract_address,
        amount_to_transfer,
        "0x",
        {"from": proposer},
    )
    tx.wait(1)  # Wait for the transaction to be mined

    # Wait for the delay period to elapse
    timelock.timelock.sleep(timelock.delay())

    # Execute the transaction
    tx = timelock.executeTransaction(
        external_contract_address,
        amount_to_transfer,
        "0x",
        {"from": proposer},
    )
    tx.wait(1)  # Wait for the transaction to be mined

    print(f"Transferred {amount_to_transfer} to {external_contract_address}")
   