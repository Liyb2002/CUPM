"""CollateralToken:csToken"""
import sys

from .tx2re import transaction2receipt

class csTokenRepo:
    def __init__(self, w3, collateralTokenContract):
        self.collateralToken = collateralTokenContract
        self.w3 = w3
    
    def mint(self, account, amount,account_admin, account_admin_key, sappropriate_gas_amount):
        tx = self.collateralToken.functions.mint(account, amount).buildTransaction()
        tx_receipt = transaction2receipt(self.w3, tx, account_admin, account_admin_key, sappropriate_gas_amount)
        return tx_receipt['contractAddress']

    def approve(self, spender, amount, fromAccount, fromAccount_key, appropriate_gas_amount = 1000000):
        tx = self.collateralToken.functions.approve(spender, amount).buildTransaction({ 'from': fromAccount})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccount, fromAccount_key, appropriate_gas_amount)
        return tx_receipt['contractAddress']
    
    def transfer(self, recipient, amount, fromAccount, fromAccount_key,appropriate_gas_amount):
        tx = self.collateralToken.functions.transfer(recipient, amount).buildTransaction({ 'from': fromAccount})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccount, fromAccount_key, appropriate_gas_amount)
        return tx_receipt['contractAddress']
    
    def transferFrom(self, sender, recipient, amount, fromAccount, fromAccount_key,appropriate_gas_amount):
        tx = self.collateralToken.functions.transferFrom(sender, recipient, amount).buildTransaction({ 'from': fromAccount})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccount, fromAccount_key, appropriate_gas_amount)
        return tx_receipt['contractAddress']
    
    def decreaseAllowance(self, spender, subtractedValue, fromAccount, fromAccount_key,appropriate_gas_amount):
        tx = self.collateralToken.functions.decreaseAllowance(spender, subtractedValue).buildTransaction({ 'from': fromAccount})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccount, fromAccount_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']
    
    def increaseAllowance(self, spender, subtractedValue, fromAccount, fromAccount_key,appropriate_gas_amount):
        tx = self.collateralToken.functions.increaseAllowance(spender, subtractedValue).buildTransaction({ 'from': fromAccount})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccount, fromAccount_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']
    
    def balanceOf(self, account):
        return self.collateralToken.functions. balanceOf(account).call()
    
    def allowance(self, owner, spender):
        return self.collateralToken.functions.allowance(owner, spender).call()
    
    def decimals(self):
        return self.collateralToken.functions.decimals().call()
    
    def name(self):
        return self.collateralToken.functions.name().call()
    
    def symbol(self):
        return self.collateralToken.functions.symbol().call()
    
    def totalSupply(self):
        return self.collateralToken.functions.totalSupply().call()
    
    def getAddress(self):
        return self.collateralToken.address