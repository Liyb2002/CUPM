"""whitelist"""

import sys

from .tx2re import transaction2receipt

class whitelistRepo:
    def __init__(self, w3, whitelistContract):
        self.whitelist = whitelistContract
        self.w3 = w3
        
    def addToWhitelist(self, usersAddressList,account_admin, account_admin_key, sappropriate_gas_amount):
        tx = self.whitelist.functions.addToWhitelist(usersAddressList).buildTransaction()
        tx_receipt = transaction2receipt(self.w3,tx, account_admin, account_admin_key, sappropriate_gas_amount)
        return tx_receipt['contractAddress']

    def removeFromWhitelist(self, usersAddressList,account_admin, account_admin_key, sappropriate_gas_amount):
        tx = self.whitelist.functions.removeFromWhitelist(usersAddressList).buildTransaction()
        tx_receipt = transaction2receipt(self.w3, tx, account_admin, account_admin_key, sappropriate_gas_amount)
        return tx_receipt['contractAddress']

    def transferOwnership(self, neOwnerAddress,account_admin, account_admin_key, sappropriate_gas_amount):
        tx = self.whitelist.functions.transferOwnership(neOwnerAddress).buildTransaction()
        tx_receipt = transaction2receipt(self.w3, tx, account_admin, account_admin_key, sappropriate_gas_amount)
        return tx_receipt['contractAddress']

    def renounceOwn(self,account_admin, account_admin_key, sappropriate_gas_amount):
        tx = self.whitelist.functions.renounceOwn().buildTransaction()
        tx_receipt = transaction2receipt(self.w3, tx, account_admin, account_admin_key, sappropriate_gas_amount)
        return tx_receipt['contractAddress']
    # 
    def isWhitelisted(self, account):
        return self.whitelist.functions.isWhitelisted(account).call()
    def owner(self):
        return self.whitelist.functions.owner().call()
    def getAddress(self):
        return self.whitelist.address