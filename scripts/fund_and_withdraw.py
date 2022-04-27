from brownie import FundMe
from scripts.helpful_scripts import get_account


def fund():

    fund_me = FundMe[-1]
    account = get_account()

    entrance_fee = fund_me.getEnteranceFee()

    print(f"The current entrance fee is {entrance_fee}")
    print("funding")
    fund_me.Fund({"from": account, "value": entrance_fee*100})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()

    # entrance_fee = fund_me.getEnteranceFee()


    print("withdraw")
    fund_me.withdraw({"from": account})


def main():
    withdraw()

