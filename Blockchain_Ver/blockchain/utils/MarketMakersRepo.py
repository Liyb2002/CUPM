import sys
from .tx2re import transaction2receipt, prob2pct

class MarketMakersRepo: 
    def __init__(self, w3, lmsrmm_contract):
        self.lmsrMarketMaker = lmsrmm_contract
        self.w3 = w3
    # read functions
    ### read functions do not need args
    def getAddress(self):
        return self.lmsrMarketMaker.address
    def getCollateralToken(self):
        return self.lmsrMarketMaker.functions.collateralToken().call()
    def getpmSystem(self):
        return self.lmsrMarketMaker.functions.pmSystem().call()
    def whitelist(self):
        return self.lmsrMarketMaker.functions.whitelist().call()
    def fee(self):
        return self.lmsrMarketMaker.functions.fee().call()
    def FEE_RANGE(self):
        return self.lmsrMarketMaker.functions.FEE_RANGE().call()
    def funding(self):
        return self.lmsrMarketMaker.functions.funding().call()
    def getOwner(self):
        return self.lmsrMarketMaker.functions.owner().call()
    def stage(self):
        return self.lmsrMarketMaker.functions.stage().call()
    def atomicOutcomeSlotCount(self):
        return self.lmsrMarketMaker.functions.atomicOutcomeSlotCount().call()
    ### read functions that need args
    def calcMarginalPrice(self, outcomeIndex):
        return prob2pct(self.lmsrMarketMaker.functions.calcMarginalPrice(outcomeIndex).call())
    def calcMarketFee(self, outcomeTokenCost):
        return self.lmsrMarketMaker.functions.calcMarketFee(outcomeTokenCost).call()
    def calcNetCost(self, outcomeTokenAmounts):
        return self.lmsrMarketMaker.functions.calcNetCost(outcomeTokenAmounts).call()
    def conditionIds(self, index):
        return self.lmsrMarketMaker.functions.conditionIds(index).call()
    #def onERC1155BatchReceived(operator, address, uint256[], uint256[], bytes )
    #def onERC1155Received(operator, address, uint256, uint256, bytes )
    
    # write funcitons
    ## write functions do not need args
    def close(self, fromAccountAdmin,fromAccountAdmin_key,appropriate_gas_amount):
        tx = self.lmsrMarketMaker.functions.close().buildTransaction({ 'from': fromAccountAdmin})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccountAdmin, fromAccountAdmin_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']
    def pause(self, fromAccountAdmin,fromAccountAdmin_key,appropriate_gas_amount):
        tx = self.lmsrMarketMaker.functions.pause().buildTransaction({ 'from': fromAccountAdmin})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccountAdmin, fromAccountAdmin_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']
    def resume(self, fromAccountAdmin,fromAccountAdmin_key,appropriate_gas_amount):
        tx = self.lmsrMarketMaker.functions.resume().buildTransaction({ 'from': fromAccountAdmin})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccountAdmin, fromAccountAdmin_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']
    def withdrawFees(self, fromAccountAdmin,fromAccountAdmin_key,appropriate_gas_amount):
        tx = self.lmsrMarketMaker.functions.withdrawFees().buildTransaction({ 'from': fromAccountAdmin})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccountAdmin, fromAccountAdmin_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']
    ## write functions need args
    def transferOwnership(self,newOwnerAddress, fromAccountAdmin,fromAccountAdmin_key,appropriate_gas_amount):
        tx = self.lmsrMarketMaker.functions.transferOwnership(newOwnerAddress).buildTransaction({ 'from': fromAccountAdmin})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccountAdmin, fromAccountAdmin_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']
    def changeFee(self, fee, fromAccountAdmin,fromAccountAdmin_key,appropriate_gas_amount):
        tx = self.lmsrMarketMaker.functions.changeFee(fee).buildTransaction({ 'from': fromAccountAdmin})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccountAdmin, fromAccountAdmin_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']
    def changeFunding(self, fundingChange, fromAccountAdmin,fromAccountAdmin_key,appropriate_gas_amount):
        tx = self.lmsrMarketMaker.functions.changeFunding(fundingChange).buildTransaction({ 'from': fromAccountAdmin})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccountAdmin, fromAccountAdmin_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']
    ##
    def trade(self, outcomeTokenAmounts, cost, fromAccount, fromAccount_key,appropriate_gas_amount):
        tx = self.lmsrMarketMaker.functions.trade(outcomeTokenAmounts, cost).buildTransaction({'from': fromAccount})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccount, fromAccount_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']