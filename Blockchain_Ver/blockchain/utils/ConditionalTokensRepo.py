"""ConditionalTokens"""
import sys

from .tx2re import transaction2receipt

class ConditionalTokensRepo:
    """ConditionalTokens implementing the solidity contract functions 
    """
    def __init__(self, w3, conditionalTokens_contract):
        self.conditionalTokens = conditionalTokens_contract
        self.w3 = w3

    # write functions
    def prepareCondition(self, oracle, questionId, outcomeSlotCount,account_admin, account_admin_key, sappropriate_gas_amount):
        """okay"""
        tx = self.conditionalTokens.functions.prepareCondition(oracle, questionId, outcomeSlotCount).buildTransaction()
        tx_receipt = transaction2receipt(self.w3, tx, account_admin, account_admin_key, sappropriate_gas_amount)
        return tx_receipt['contractAddress']
    
    def splitPosition(self, collateralToken, parentCollectionId, conditionId, partitions, amount,account_admin, account_admin_key, sappropriate_gas_amount):
        """okay"""
        tx = self.conditionalTokens.functions.splitPosition(collateralToken, parentCollectionId, conditionId, partitions, amount).buildTransaction()
        tx_receipt = transaction2receipt(self.w3, tx, account_admin, account_admin_key, sappropriate_gas_amount)
        return tx_receipt['contractAddress']
    
    def mergePositions(self, collateralToken, parentCollectionId, conditionId, partitions, amount,account_admin, account_admin_key, sappropriate_gas_amount):
        """"""
        tx = self.conditionalTokens.functions.mergePositions(collateralToken, parentCollectionId, conditionId, partitions, amount).buildTransaction()
        tx_receipt = transaction2receipt(self.w3, tx, account_admin, account_admin_key, sappropriate_gas_amount)
        return tx_receipt['contractAddress']

    def setApprovalForAll(self, lmsrMarketMakerAddress, approved, fromAccount, fromAccount_key, appropriate_gas_amount):
        """"""
        tx = self.conditionalTokens.functions.setApprovalForAll(lmsrMarketMakerAddress, approved).buildTransaction({'from': fromAccount})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccount, fromAccount_key, appropriate_gas_amount)
        return tx_receipt['contractAddress']

    def reportPayouts(self, questionId, payouts,account_admin, account_admin_key, sappropriate_gas_amount):
        """"""
        print('reporting payouts: {}'.format(questionId))
        tx = self.conditionalTokens.functions.reportPayouts(questionId, payouts).buildTransaction()
        tx_receipt = transaction2receipt(self.w3, tx, account_admin, account_admin_key, sappropriate_gas_amount)
        return tx_receipt['contractAddress']

    def redeemPositions(self, collateralAddress, parentCollectionId, marketConditionId, indexSets, fromAccount, fromAccount_key,appropriate_gas_amount):
        """"""
        tx = self.conditionalTokens.functions.redeemPositions(collateralAddress, parentCollectionId, marketConditionId, indexSets).buildTransaction({'from': fromAccount})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccount, fromAccount_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']

    def safeTransferFrom(self, fromAccount, toAccount, positionId, amount, data, fromAccount_key, appropriate_gas_amount):
        """"""
        tx = self.conditionalTokens.functions.safeTransferFrom(fromAccount, toAccount, positionId, amount, data).buildTransaction({'from': fromAccount})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccount, fromAccount_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']

    def safeBatchTransferFrom(self, fromAccount, toAccount, positionIds, amounts, data, fromAccount_key, appropriate_gas_amount):
        """"""
        tx = self.conditionalTokens.functions.safeTransferFrom(fromAccount, toAccount, positionIds, amounts, data).buildTransaction({'from': fromAccount})
        tx_receipt = transaction2receipt(self.w3, tx, fromAccount, fromAccount_key,appropriate_gas_amount)
        return tx_receipt['contractAddress']

    # read functions
    def balanceOf(self, account, positionId):
        """balanceOf(msg.sender, positionId)"""
        return self.conditionalTokens.functions.balanceOf(account, positionId).call()
    def balanceOfBatch(self, accounts, positionIds):
        return self.conditionalTokens.functions.balanceOfBatch(accounts, positionIds).call()
    # 1: getConditionId => prepareCondition => getOutcomeSlotCount
    def getConditionId(self, account_admin, questionId, outcomeSlotCount):
        """CTHelpers.getConditionId(msg.sender, questionId, outcomeSlotCount)"""
        return self.conditionalTokens.functions.getConditionId(account_admin, questionId, outcomeSlotCount).call()
    def getOutcomeSlotCount(self, conditionId):
        return self.conditionalTokens.functions.getOutcomeSlotCount(conditionId).call()
    # 2: getCollectionId => getPositionId => splitPosition => reportPayouts => redeemPositions
    def getCollectionId(self, parentCollectionId, conditionId , indexSet):
        return self.conditionalTokens.functions.getCollectionId(parentCollectionId, conditionId, indexSet).call()
    def getPositionId(self, collateralToken, collectionId):
        return self.conditionalTokens.functions.getPositionId(collateralToken, collectionId).call()
    def payoutDenominator (self, conditionId):
        return self.conditionalTokens.functions.payoutDenominator(conditionId).call()
    def payoutNumerators(self, conditionId, outcomeIndex):
        return self.conditionalTokens.functions.payoutNumerators(conditionId, outcomeIndex).call()
    def isApprovedForAll(self, account, operator):
        """operator: lmsrMarketMaker owner"""
        return self.conditionalTokens.functions.isApprovedForAll(account, operator).call()
    def getAddress(self):
        return self.conditionalTokens.address