from brownie import FundMe, MockV3Aggregator, network, config


from scripts.helpful_scripts import get_account, deploy_mocks,LOCAL_BLOCKCHAIN_ENVIRONEMNTS
from web3 import Web3

# if we are on a persisitent network like rinkeby, use the assciated address
# otherwish deploy mocks


def deploy_fund_me():
    account = get_account()
    print("-------------",network.show_active())
    # pass the price feed address to fundme contract

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONEMNTS:
        price_feed_adress = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    
    else:
        deploy_mocks()
        price_feed_adress = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_adress,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verfiy"),
    )

    print(f"Contract deployed to {fund_me.address}")

    return fund_me
    


def main():
    deploy_fund_me()
