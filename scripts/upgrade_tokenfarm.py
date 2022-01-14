from scripts.helpful_scripts import get_account, get_contract, encode_function_data, upgrade
from brownie import MockToken, TokenFarmV3, network, config, ProxyAdmin, TransparentUpgradeableProxy, Contract, exceptions
from web3 import Web3
import yaml
import json
import os
import shutil

def upgrade_tokenfarm():
    account = get_account()
    # tokenfarm_v3 = TokenFarmV3.deploy({"from": account}, publish_source = True)
    proxy_admin_address = "0xe2Edd99960c49C40c16A500c7A69cA8b34dd16C7"
    proxy_address = "0xDB141CfbcCD86004AdBBd02A7c6399DFaC3844c7"
    mock_token_address = "0x9cf4aE8522727f1ca6d951750Cc240F65572e484"
    
    proxy_admin = Contract.from_abi("ProxyAdmin", proxy_admin_address, ProxyAdmin.abi)
    proxy = Contract.from_abi("TransparentUpgradeableProxy", proxy_address, TransparentUpgradeableProxy.abi)
    
    # upgrade_transaction = upgrade(
    #     account, 
    #     proxy, 
    #     tokenfarm_v3.address,
    #     proxy_admin_contract=proxy_admin,
    # )
    # upgrade_transaction.wait(1)
    # print("Proxy has been upgrade!")
    
    proxy_farm = Contract.from_abi("TokenFarmV3", proxy_address, TokenFarmV3.abi)
    # init_px = proxy_farm.initialize(mock_token_address, account, {"from": account})
    # init_px.wait(1)
    
    total = proxy_farm.getUserTotalValueV3(account, {"from": account})
    print(total)
    
    
    
def main():
    upgrade_tokenfarm()