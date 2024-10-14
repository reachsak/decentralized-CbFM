from brownie import MoralisGovernor, accounts

def main():
    # Load the MoralisGovernor contract
#timelock contract is the DAO contract
    address = "0x1F5Ef6e65d00247e4149C274Eb68B718343161A2"
    balance = accounts.at(address, force=True).balance()
    balance_in_ether = balance / 10**18
    print(f"Balance of address {address}: {balance_in_ether} Ether")
#0xdE055E82D26A901076168E546C36ac67B755C92F


main()