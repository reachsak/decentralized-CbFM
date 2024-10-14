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


def propose(store_value,amount):
    account = get_account()
    args = (store_value,amount)
    encoded_function = Contract.from_abi("TimeLock", TimeLock[-1], TimeLock.abi).sendEther.encode_input(
        *args
    )
    print(encoded_function)
    propose_tx = MoralisGovernor[-1].propose(
        [TimeLock[-1].address],
        [0],
        [encoded_function],
        PROPOSAL_DESCRIPTION,
        {"from": account},
    )
    # if network.show_active() == "development":
    #     tx = account.transfer(accounts[0], "0.1 ether")
    #     tx.wait(1)
    tx = account.transfer(accounts[0], "0.01 ether")
    tx.wait(1)
        
    propose_tx.wait(2)
    proposal_id = propose_tx.events["ProposalCreated"]["proposalId"]
    print(f"Proposal State {MoralisGovernor[-1].state(proposal_id)}")
    print(f"Proposal Snapshot {MoralisGovernor[-1].proposalSnapshot(proposal_id)}")
    print(f"Proposal deadline {MoralisGovernor[-1].proposalDeadline(proposal_id)}")

    return proposal_id




def main():
    amount=30000000000000000
    proposal_id=propose(STORE_VALUE,amount)
    print(proposal_id)
    ##original
    #proposal_id = propose(STORE_VALUE)
    #print(f"proposal id: {proposal_id}")
    #vote(proposal_id, 1)
    ##114771710093733580986057710226004826369550559628955805013962745724685072316577
    ##vote(114771710093733580986057710226004826369550559628955805013962745724685072316577, 1)
    ##queue_and_execute(STORE_VALUE,1000000000)

    
