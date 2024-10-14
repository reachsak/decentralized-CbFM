from brownie import web3
from brownie import (
    MoralisGovernor,
    TimeLock,
    Box,
    GovernanceToken,
    network,
    config,
    Contract,
    accounts,
    chain,
)
from scripts.helpful_scripts import get_account
from scripts.deploy_contracts import deploy_contracts
from web3 import Web3
import time
# Replace '0xdE055E82D26A901076168E546C36ac67B755C92F' with the actual DAO contract address
dao_address = '0xdE055E82D26A901076168E546C36ac67B755C92F'
account = get_account()

# Amount of Ether to send (in Wei)
amount_in_wei = web3.to_wei(0.1, 'ether')

# Send Ether to the DAO contract address
tx = accounts[0].transfer(dao_address, amount_in_wei)

# Wait for the transaction to be mined
tx.wait(1)

print("Ether sent to DAO address successfully.")