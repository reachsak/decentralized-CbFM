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

STORE_VALUE = "0x8b6f8EAA942A983AD887676fcB8c488379796410"

VOTING_PERIOD = 1  # 1 hour

#order 
##deploy, propose ,vote, execute
def execute_proposal():
    proposal_id = propose(STORE_VALUE)
    print(f"proposal id: {proposal_id}")
    queue_and_execute(STORE_VALUE,100000000)


def propose(store_value):
    account = get_account()
    args = (store_value,)
    encoded_function = Contract.from_abi("Box", Box[-1], Box.abi).store.encode_input(
        *args
    )
    print(encoded_function)
    propose_tx = MoralisGovernor[-1].propose(
        [Box[-1].address],
        [0],
        [encoded_function],
        PROPOSAL_DESCRIPTION,
        {"from": account},
    )
    # if network.show_active() == "development":
    #     tx = account.transfer(accounts[0], "0.1 ether")
    #     tx.wait(1)
    tx = account.transfer(accounts[0], "0.1 ether")
    tx.wait(1)
        
    propose_tx.wait(2)
    proposal_id = propose_tx.events["ProposalCreated"]["proposalId"]
    print(f"Proposal State {MoralisGovernor[-1].state(proposal_id)}")
    print(f"Proposal Snapshot {MoralisGovernor[-1].proposalSnapshot(proposal_id)}")
    print(f"Proposal deadline {MoralisGovernor[-1].proposalDeadline(proposal_id)}")

    return proposal_id


def vote(proposal_id: int, vote: int):
    # 0 => Against, 1 => For, 2 => Abstain
    print(f"Voting yes on {proposal_id}")
    account = get_account()
    tx = MoralisGovernor[-1].castVoteWithReason(
        proposal_id, vote, "I vote yes because reasons...", {"from": account}
    )
    tx.wait(1)
    print(tx.events["VoteCast"])


def queue_and_execute(store_value,gas_limit):
    account = get_account()
    args = (store_value,)
    encoded_function = Contract.from_abi("MoralisGovernor", MoralisGovernor[-1], MoralisGovernor.abi).addMember.encode_input(
        *args
    )
    # description hash
    description_hash = Web3.keccak(text=PROPOSAL_DESCRIPTION).hex()
    tx = MoralisGovernor[-1].queue(
        [MoralisGovernor[-1].address],
        [0],
        [encoded_function],
        description_hash,
        {"from": account,"gas_limit":gas_limit,}
    )

    tx.wait(1)

    # if network.show_active() == "development":



def main():
    queue_and_execute(STORE_VALUE,300000)
    ##original
    #proposal_id = propose(STORE_VALUE)
    #print(f"proposal id: {proposal_id}")
    #vote(proposal_id, 1)
    ##114771710093733580986057710226004826369550559628955805013962745724685072316577
    ##vote(114771710093733580986057710226004826369550559628955805013962745724685072316577, 1)
    ##queue_and_execute(STORE_VALUE,1000000000)

    
