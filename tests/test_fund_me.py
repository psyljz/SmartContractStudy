from brownie import accounts, network,exceptions
from scripts.helpful_scripts import get_account,LOCAL_BLOCKCHAIN_ENVIRONEMNTS
from scripts.deploy import deploy_fund_me
import pytest

def test_fund():
    # Arrange


    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEnteranceFee()

    print(f"The current entrance fee is {entrance_fee}")
    # Act
    
    
   
    txn= fund_me.Fund({"from": account, "value": entrance_fee})
    txn.wait(1)
    # Assert

    assert  fund_me.addressToamountFunded(account.address)==entrance_fee
    txn2 =fund_me.withdraw({"from":account})

    txn2.wait(1)
    assert fund_me.addressToamountFunded(account.address)==0

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONEMNTS:
        pytest.skip("only for local testing")
    account =get_account()
    fund_me =deploy_fund_me()
    bad_actor =accounts.add()
    
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from":bad_actor})