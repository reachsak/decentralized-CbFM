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
    Transfer,
)
from scripts.helpful_scripts import get_account
from scripts.deploy_contracts import deploy_contracts
from web3 import Web3
import time


def vote(proposal_id: int, vote: int):
    # 0 => Against, 1 => For, 2 => Abstain
    print(f"Voting yes on {proposal_id}")
    account = get_account()
    tx = MoralisGovernor[-1].castVoteWithReason(
        proposal_id, vote, "I vote yes because reasons...", {"from": account}
    )
    tx.wait(1)
    print(tx.events["VoteCast"])


def main():
    proposal_id =86128036329659314973352279677055470624315565080980238686043800690141424593162
    vote(proposal_id, 1)
    #move_blocks(6)
    
    #queue_and_execute(recipient,amount_to_send,300000)
    ##original
    #proposal_id = propose(STORE_VALUE)
    #print(f"proposal id: {proposal_id}")
    #vote(proposal_id, 1)
    ##114771710093733580986057710226004826369550559628955805013962745724685072316577
    ##vote(114771710093733580986057710226004826369550559628955805013962745724685072316577, 1)
    ##queue_and_execute(STORE_VALUE,1000000000)

    
