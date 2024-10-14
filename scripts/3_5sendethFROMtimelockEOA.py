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


def checkstate(receiver, amount):
    # 0 => Against, 1 => For, 2 => Abstain
    print(f"sending {amount} Ether from TimeLock contract to {receiver}")
    account = get_account()
    timelock = TimeLock[-1]
    tx = timelock.sendEther(receiver, amount,{"from": account})
    tx.wait(1)
    print(tx)
    print("sending done")

def main():
    proposal_id = 20000000000000000
    receiver = "0xC9602ab8682443e3e0391Aa9b86E0360479B85C2"
    amount = proposal_id  # Assuming amount is the same as proposal_id
    checkstate(receiver, amount)
    ##original
    #proposal_id = propose(STORE_VALUE)
    #print(f"proposal id: {proposal_id}")
    #vote(proposal_id, 1)
    ##114771710093733580986057710226004826369550559628955805013962745724685072316577
    ##vote(114771710093733580986057710226004826369550559628955805013962745724685072316577, 1)
    ##queue_and_execute(STORE_VALUE,1000000000)

    
