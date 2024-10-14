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

PROPOSAL_DESCRIPTION = "Store a value in the Box contract."

STORE_VALUE = "0xC9602ab8682443e3e0391Aa9b86E0360479B85C2"

VOTING_PERIOD = 1  # 1 hour

#order 
##deploy, propose ,vote, execute


def queue_and_execute(store_value,gas_limit,amount):
    account = get_account()
    args = (store_value,amount)
    encoded_function = Contract.from_abi("TimeLock", TimeLock[-1], TimeLock.abi).sendEther.encode_input(
        *args
    )
    # description hash
    description_hash = Web3.keccak(text=PROPOSAL_DESCRIPTION).hex()
    tx = MoralisGovernor[-1].execute(
        [TimeLock[-1].address],
        [0],
        [encoded_function],
        description_hash,
        {"from": account,"gas_limit":gas_limit,}
    )

    tx.wait(1)

    # if network.show_active() == "development":



def main():
    amount=30000000000000000
    queue_and_execute(STORE_VALUE,300000,amount)
    ##original
    #proposal_id = propose(STORE_VALUE)
    #print(f"proposal id: {proposal_id}")
    #vote(proposal_id, 1)
    ##114771710093733580986057710226004826369550559628955805013962745724685072316577
    ##vote(114771710093733580986057710226004826369550559628955805013962745724685072316577, 1)
    ##queue_and_execute(STORE_VALUE,1000000000)

    
