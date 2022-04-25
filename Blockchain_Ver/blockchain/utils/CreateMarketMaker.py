
import json
from web3.logs import STRICT, IGNORE, DISCARD, WARN

class CreateMarketMaker:
    """ create a new market
    input: contracts, marketConf
    return: a new market address
    """
    def __init__(self, w3, contracts):
        self.w3 = w3
        self.whitelist = contracts['whitelist_py']
        self.csToken = contracts['csToken_py']
        self.ConditionalTokens = contracts['ConditionalTokens_py']
        self.lmsrmmf = contracts['lmsrmmf_py']
        self.lmsrmmf_contract = contracts['lmsrmmf_contract']
        self.lmsrmm_json = contracts['lmsrmm_json']

    def createMM(self, marketConf, account_admin, private_key, appropriate_gas_amount):
        # how to clear all whitelist participants
        whitelistAddress = self.whitelist.getAddress()
        # print(f'whitelistAddress:{whitelistAddress}')
        csTokenAddress = self.csToken.getAddress()
        ConditionalTokensAddress = self.ConditionalTokens.getAddress()
        lmsrmmfAddress = self.lmsrmmf.getAddress()
        lmsrmmConf = marketConf
        lmsrmmConf['whitelistAddress'] = whitelistAddress

        try:
            self.ConditionalTokens.prepareCondition(account_admin, marketConf['questionId'], marketConf['slotNumber'], account_admin, private_key, 100000)
        except:
            pass
           
        conditionId = self.ConditionalTokens.getConditionId(account_admin, marketConf['questionId'], marketConf['slotNumber'])
        
        # try:
        #     conditionId = self.ConditionalTokens.getConditionId(account_admin, marketConf['questionId'], marketConf['slotNumber'])
        # except:
        #     self.ConditionalTokens.prepareCondition(account_admin, marketConf['questionId'], marketConf['slotNumber'], account_admin, private_key, 100000)
        #     conditionId = self.ConditionalTokens.getConditionId(account_admin, marketConf['questionId'], marketConf['slotNumber'])
        try:
            print(f'getOutcomeSlotCount: {self.ConditionalTokens.getOutcomeSlotCount(conditionId)}')
        except:
            print('market has not been prepared')
        
        # get 2 slot market: collectionId, PositionId
        # get ids for 2 slot market
        # - Lo:1 0 -> 0b01 == 1
        # - Hi:0 1 -> 0b10 == 2

        parentCollectionId = '0x0000000000000000000000000000000000000000000000000000000000000000'
        collectionIdLo = self.ConditionalTokens.getCollectionId(parentCollectionId, conditionId , 1)
        collectionIdHi = self.ConditionalTokens.getCollectionId(parentCollectionId, conditionId , 2)
        positionIdLo = self.ConditionalTokens.getPositionId(csTokenAddress, collectionIdLo)
        positionIdHi = self.ConditionalTokens.getPositionId(csTokenAddress, collectionIdHi)

        lmsrmmConf['collectionIdLo'] = collectionIdLo
        lmsrmmConf['collectionIdHi'] = collectionIdHi 
        lmsrmmConf['positionIdLo'] = positionIdLo
        lmsrmmConf['positionIdHi'] = positionIdHi
        #
        # print(f'conditionId:{conditionId}')
        # check balance and allowance
        print("check balance and alloance")
        balanceOfsender = self.csToken.balanceOf(account_admin)
        if balanceOfsender < marketConf['ammFunding']:
            self.csToken.mint(account_admin, marketConf['ammFunding'], account_admin, private_key, appropriate_gas_amount)
        #
        spenderAllowance = self.csToken.allowance(account_admin, lmsrmmfAddress)
        if spenderAllowance < marketConf['ammFunding']:
            print('insufficient allowance')
            self.csToken.approve(lmsrmmfAddress, marketConf['ammFunding'], account_admin, private_key, 1000000)

        print('create lmsr market')
        tx_receipt = self.lmsrmmf.createLMSRMarketMaker(ConditionalTokensAddress,
                                        csTokenAddress,
                                        [conditionId],
                                        marketConf['fee'],
                                        whitelistAddress,
                                        marketConf['ammFunding'],
                                        account_admin,
                                        private_key,
                                        1000000)
        creationLogEntry = self.lmsrmmf_contract.events.LMSRMarketMakerCreation().processReceipt(tx_receipt, errors=DISCARD)
        lmsrAddress = creationLogEntry[0].args.lmsrMarketMaker
        lmsrmmConf['lmsrAddress'] = lmsrAddress
        lmsrmmConf['creator'] = creationLogEntry[0].args.creator
        #csTokenAddress = creationLogEntry[0].args.collateralToken
        lmsrmmConf['csTokenAddress'] = csTokenAddress
        #ConditionalTokensAddress = creationLogEntry[0].args.pmSystem
        lmsrmmConf['ConditionalTokensAddress'] = ConditionalTokensAddress
        conditionId = creationLogEntry[0].args.conditionIds[0]
        lmsrmmConf['conditionId'] = conditionId

        # update lmsrMarketMaker
        with open(self.lmsrmm_json, 'r') as f:
                datastore = json.load(f)
                abi = datastore["abi"]
                contract_address = lmsrAddress
                lmsrMarketMaker_contract = self.w3.eth.contract(address=contract_address,abi=abi)
        lmsrmmConf['lmsrmm_contract'] = lmsrMarketMaker_contract
        # lmsrmmConf['csToken_contract'] = self.csToken_json
        # lmsrmmConf['ConditionalTokens_contract'] = self.ConditionalTokens_json
        return lmsrmmConf