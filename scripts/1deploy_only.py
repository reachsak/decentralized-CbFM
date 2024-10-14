from brownie import (
    MoralisGovernor,
    TimeLock,
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
VOTING_DELAY = 1  # 1 block

# TimeLock
MIN_DELAY = 0  # Seconds

# Address 0
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def deploy_contracts():
    account = get_account()
    governance_token = (
        GovernanceToken.deploy(20,
            {"from": account},
        )
        if len(GovernanceToken) <= 0
        else GovernanceToken[-1]
    )
    print(f"Governance Token: {governance_token.address}")
    
    governance_token.delegate(account, {"from": account})


    governance_time_lock = TimeLock.deploy(
        MIN_DELAY,
        [],
        [],
        account,
        {"from": account},
    )

    print(f"Governance TimeLock: {governance_time_lock.address}")
    governor = MoralisGovernor.deploy(
        governance_token.address,#### there are problem here, sometime it requier .address, sometime it doesn't require .addresss , but most of the time, having .address will work, allow me to go all the way to execute part
        governance_time_lock.address,
        QUORUM_PERCENTAGE,
        VOTING_PERIOD,
        VOTING_DELAY,
        {"from": account},

    )

    # Setting Up the Roles.

    proposer_role = governance_time_lock.PROPOSER_ROLE()
    executor_role = governance_time_lock.EXECUTOR_ROLE()
    timelock_admin_role = governance_time_lock.TIMELOCK_ADMIN_ROLE()
    governance_time_lock.grantRole(proposer_role, governor.address, {"from": account})
    governance_time_lock.grantRole(executor_role, ZERO_ADDRESS, {"from": account})
    governance_time_lock.grantRole(timelock_admin_role, account, {"from": account})


    box = Box.deploy({"from": account})
    tx = box.transferOwnership(TimeLock[-1], {"from": account})##### lots time , it will fail here too, maybe the timelock don't have any account , so calling -1 will fail, so basically neeed to  restart that 
    tx.wait(1)



def main():
    deploy_contracts()
