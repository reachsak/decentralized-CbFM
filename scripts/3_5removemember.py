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


def checkstate(proposal_id: int):
    # 0 => Against, 1 => For, 2 => Abstain
    print(f"adding member {proposal_id}")
    account = get_account()
    tx = MoralisGovernor[-1].removeMember(
        proposal_id, {"from": account}
    )

    print(tx)
    print("adding done")


#34546435337505149170984682677621345131795101285630670478253744488918325444400
def main():
    proposal_id ="0xb8020dADD99d75F9806fc0B97648cFe5Dc186541"
    checkstate(proposal_id)
    ##original
    #proposal_id = propose(STORE_VALUE)
    #print(f"proposal id: {proposal_id}")
    #vote(proposal_id, 1)
    ##114771710093733580986057710226004826369550559628955805013962745724685072316577
    ##vote(114771710093733580986057710226004826369550559628955805013962745724685072316577, 1)
    ##queue_and_execute(STORE_VALUE,1000000000)

    
