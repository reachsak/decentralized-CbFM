from brownie import (
    MoralisGovernor,
    TimeLock,
    ProposalContract,
    Box,
    EtherTransfer,
    Transfer,
    GovernanceToken,
    network,
    config,
    Contract,
)
from scripts.helpful_scripts import get_account

from web3 import Web3

initial_supply = Web3.from_wei(1000, "ether")


QUORUM_PERCENTAGE = 1  # %
VOTING_PERIOD = 5  # block
VOTING_DELAY = 0  # 1 block

# TimeLock
MIN_DELAY = 0  # Seconds

# Address 0
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def deploy_contracts():
    account = get_account()


    governance_time_lock = ProposalContract.deploy({"from": account}
    )

    print(f"proposaltype address: {governance_time_lock.address}")



def main():
    deploy_contracts()
