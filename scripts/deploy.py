from scripts.helpful_scripts import get_account, get_contract, encode_function_data
from brownie import MockToken, TokenFarmUP, network, config, ProxyAdmin, TransparentUpgradeableProxy, Contract, exceptions
from web3 import Web3
import yaml
import json
import os
import shutil


KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_token_farm_and_mock_token(update_front_end=False):
    account = get_account()
    mock_token = MockToken.deploy({"from": account})
    print("mock token2 deployed")
    token_farm = TokenFarmUP.deploy( 
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"]
    )
    print("token_farm deployed")
    print(token_farm)
    
    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source = True
                                    )
    print("proxy admin deployed")
    # initializer = token_farm.initialize 
    farm_encoded_initializer_function = encode_function_data()
    
    proxy = TransparentUpgradeableProxy.deploy(
        token_farm.address,
        proxy_admin.address,
        farm_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000}, publish_source = True
    )
    print("proxy deployed")
    tx = mock_token.transfer(
        proxy.address, mock_token.totalSupply() - KEPT_BALANCE,
        {"from": account}
    )
    tx.wait(1)
    
    # trafer_own = token_farm.transferOwnership(proxy.address, {"from": account})
    # trafer_own.wait(1)
    # print("owner tranfer")
    
    proxy_farm = Contract.from_abi("TokenFarmP", proxy.address, TokenFarmUP.abi)
    
    #### Test ####
    init_px = proxy_farm.initialize(mock_token.address, account, {"from": account})
    init_px.wait(1)
    
    own, send, res = proxy_farm.checkOwner({"from": account})
    # test_const.wait(1)
    print(f"own: {own}, send: {send}, res: {res}")
    
    # mock_token, weth_token, fau_token/dai
    # weth_token = config[""]
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    dict_of_allowed_tokens = {
        mock_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed") 
    }
    add_allowed_tokens(proxy_farm, dict_of_allowed_tokens, account)
    if update_front_end:
        update_front_end()
    return proxy_farm, mock_token
    
    
def add_allowed_tokens(proxy_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = proxy_farm.AddAllowedTokens(token.address, {"from": account, "gas_limit": 1000000, "allow_revert":True})
        add_tx.wait(1)
        set_tx = proxy_farm.setPriceFeedContract(token.address,
                                                dict_of_allowed_tokens[token],
                                                {"from": account, "gas_limit": 1000000, "allow_revert":True}
        )
        set_tx.wait(1)
    return proxy_farm

def update_front_end():
    copy_folders_to_front_end(src="./build", dest="./front_end/src/chain-info")
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open("./brownie-config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json)
    print("front end update")
    
    
def copy_folders_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def main():
    deploy_token_farm_and_mock_token(update_front_end=False)