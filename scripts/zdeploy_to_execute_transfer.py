from brownie import (
    MoralisGovernor,
    TimeLock,
    Transfer,
    Box,
    GovernanceToken,
    network,
    config,
    Contract,
    accounts,
    chain,
)
from scripts.helpful_scripts import get_account

from web3 import Web3
import time

PROPOSAL_DESCRIPTION = "Store a value in the Box contract."

STORE_VALUE = 10

VOTING_PERIOD = 10 # 1 hour

#order 
##deploy, propose ,vote, execute

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
MIN_DELAY = 5  # Seconds

# Address 0
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def deploy_contracts():
    account = get_account()
    governance_token = (
        GovernanceToken.deploy(
            {"from": account},
        )
        if len(GovernanceToken) <= 0
        else GovernanceToken[-1]
    )
    
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

    # Deploying Contract to be Governed.
    ## this is important , i will write my own contract here
    transfer = Transfer.deploy({"from": account})
    print(f"Transfer Contract Address: {transfer.address}")
    print("Transfer deployed")

    box = Box.deploy({"from": account})
    tx = box.transferOwnership(TimeLock[-1], {"from": account})##### lots time , it will fail here too, maybe the timelock don't have any account , so calling -1 will fail, so basically neeed to  restart that 
    tx.wait(1)


PROPOSAL_DESCRIPTION = "Store a value in the Box contract."
recipient = "0xC9602ab8682443e3e0391Aa9b86E0360479B85C2"
amount_to_send = Web3.to_wei(0.05, "ether")  # Specify the amount of Ether to send

def propose_transfer(recipient, amount):
    account = get_account()
    encoded_function = (
        Contract.from_abi("Transfer", Transfer[-1].address, Transfer.abi)
        .transferEther.encode_input(recipient, amount)  # Include the amount parameter
    )
    propose_tx = MoralisGovernor[-1].propose(
        [Transfer[-1].address],
        [0],
        [encoded_function],
        PROPOSAL_DESCRIPTION,
        {"from": account},
    )
    propose_tx.wait(2)
    proposal_id = propose_tx.events["ProposalCreated"]["proposalId"]
    print(f"Proposal State: {MoralisGovernor[-1].state(proposal_id)}")
    return proposal_id



def execute_proposal():
    deploy_contracts()
    proposal_id = propose_transfer(recipient, amount_to_send)
    print(f"proposal id: {proposal_id}")
    vote(proposal_id, 1) ### need to vote here in frontend, otherwise, it will show ,proposal not sucessful, don't put it like ths, have to wait for the vote to be active , otherwise it will be error 
    queue_and_execute(STORE_VALUE,100000000) ### also, this also have to wait until the voting period is ended , before i can executte , otherwise it will be error 


def vote(proposal_id: int, vote: int):
    # 0 => Against, 1 => For, 2 => Abstain
    print(f"Voting yes on {proposal_id}")
    account = get_account()
    tx = MoralisGovernor[-1].castVoteWithReason(
        proposal_id, vote, "I vote yes because reasons...", {"from": account}
    )
    tx.wait(1)
    print(tx.events["VoteCast"])

def queue_and_execute(recipient,amount_to_send,gas_limit):
    account = get_account()
    args = (recipient, amount_to_send) 

    encoded_function = (
        Contract.from_abi("Transfer", Transfer[-1].address, Transfer.abi)
        .transferEther.encode_input(*args)  # Include the amount parameter
    )
    # description hash
    description_hash = Web3.keccak(text=PROPOSAL_DESCRIPTION).hex()
    tx = MoralisGovernor[-1].queue(
        [Transfer[-1].address],
        [0],
        [encoded_function],
        description_hash,
        {"from": account,"gas_limit":gas_limit,}
    )

    tx.wait(1)
    # description hash
    description_hash = Web3.keccak(text=PROPOSAL_DESCRIPTION).hex()
    tx = MoralisGovernor[-1].execute(
        [Transfer[-1].address],
        [0],
        [encoded_function],
        description_hash,
        {"from": account,"gas_limit":gas_limit,}
    )
    
    
    
    
    
def move_blocks(amount):
    for block in range(amount):
        get_account().transfer(get_account(), "0 ether")
    print(chain.height)


def main():
    execute_proposal()
    ##original
    #proposal_id = propose(STORE_VALUE)
    #print(f"proposal id: {proposal_id}")
    #vote(proposal_id, 1)
    ##114771710093733580986057710226004826369550559628955805013962745724685072316577
    ##vote(114771710093733580986057710226004826369550559628955805013962745724685072316577, 1)
    ##queue_and_execute(STORE_VALUE,1000000000)

    
