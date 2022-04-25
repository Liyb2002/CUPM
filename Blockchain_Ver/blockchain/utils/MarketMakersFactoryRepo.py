import sys

from .tx2re import transaction2receipt, prob2pct

class MarketMakersFactoryRepo: 
    def __init__(self, w3, lmsrmmf_contract):
        self.lmsrMarketMakerFactory = lmsrmmf_contract
        self.w3 = w3
   
    # read functions
    ### read functions do not need args
    def getAddress(self):
        return self.lmsrMarketMakerFactory.address
    def implementationMaster(self):
        return self.lmsrMarketMakerFactory.functions.implementationMaster().call()
    # write functions
    def cloneConstructor(self, consData,fromAccountAdmin, fromAccountAdmin_key,appropriate_gas_amount):
        tx = self.lmsrMarketMakerFactory.functions.cloneConstructor(consData).buildTransaction({ 'from': fromAccountAdmin})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccountAdmin, fromAccountAdmin_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']
    def createLMSRMarketMaker(self, ConditionalTokensAddress, 
                              csTokenAddress, 
                              conditionIds, 
                              fee,
                              whitelist_contractAddress, 
                              ammFunding, 
                              fromAccountAdmin, 
                              fromAccountAdmin_key,
                              appropriate_gas_amount):
        tx = self.lmsrMarketMakerFactory.functions.createLMSRMarketMaker(ConditionalTokensAddress, 
                                                                         csTokenAddress, 
                                                                         conditionIds, 
                                                                         fee, 
                                                                         whitelist_contractAddress, 
                                                                         ammFunding).buildTransaction({ 'from': fromAccountAdmin})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccountAdmin, fromAccountAdmin_key,appropriate_gas_amount)
        return tx_receipt