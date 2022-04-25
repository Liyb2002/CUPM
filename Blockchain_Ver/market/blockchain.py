from requests.api import get
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from collections import defaultdict
import requests
from .models import User_Reputation, User, Comment
from blockchain.utils import CreateMarketMaker, whitelistRepo, csTokenRepo, ConditionalTokensRepo, MarketMakersRepo, MarketMakersFactoryRepo

#Copy paste everything
INFURA_KEY="2284fa6facbf424aa231f4caa4479972"
RINKEBY_MNEMONIC="section melt invest boss goose inch scatter exact sponsor north method suit unable balcony voice"
account_admin ="0x03abA998B8888A2F8bdA00e5ddb8d4a598Af69BF"
private_key="4f92235d90b5d5601ab19fc5d3a9f281e692c731bb9e5e99d073e122a454d323"
IPFS_PATH="https://ipfs.io/ipfs/QmXU5KYqNbrps9GGTBNwa3S4nLvA5jDqakN4zBUkRH2TMX?filename=PredictionMarketFactory.json"


def getWeb3():
    infura_url ="https://rinkeby.infura.io/v3/" + INFURA_KEY
    w3 = Web3(Web3.HTTPProvider(infura_url))
    w3.middleware_onion.clear()
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def getContract(file_json, w3):
    with open(file_json, 'r') as f:
        datastore = json.load(f)
        abi = datastore["abi"]
        contract_address = datastore["contract_address"]
        contract_name = w3.eth.contract(address=contract_address,abi=abi)
    return contract_name

import os
from mysite.settings import BASE_DIR

def loadContracts(w3):
    csToken_json = os.path.join(BASE_DIR,'blockchain/contracts_data/csTokendata.json')
    conditionalTokens_json = os.path.join(BASE_DIR,'blockchain/contracts_data/conditionalTokensdata.json')
    lmsrmm_json = os.path.join(BASE_DIR,'blockchain/contracts_data/lmsrmmdata.json')
    lmsrmmf_json = os.path.join(BASE_DIR,'blockchain/contracts_data/lmsrmmfdata.json')
    whitelist_json = os.path.join(BASE_DIR,'blockchain/contracts_data/whitelistdata.json')

    #get deployed solidity json
    contracts = defaultdict(lambda: "Not Present")
    contracts["whitelist_json"] = whitelist_json
    contracts["csToken_json"] = csToken_json
    contracts["ConditionalTokens_json"] = conditionalTokens_json
    contracts["lmsrmm_json"] = lmsrmm_json
    contracts["lmsrmmf_json"] = lmsrmmf_json

    #get contract instance
    contracts["whitelist_contract"] = getContract(contracts["whitelist_json"],w3)
    contracts["csToken_contract"] = getContract(contracts["csToken_json"],w3)
    contracts["ConditionalTokens_contract"] = getContract(contracts["ConditionalTokens_json"],w3)
    contracts["lmsrmm_contract"] = getContract(contracts["lmsrmm_json"],w3)
    contracts["lmsrmmf_contract"] = getContract(contracts["lmsrmmf_json"],w3)

    #get contract python function
    contracts["whitelist_py"] = whitelistRepo.whitelistRepo(w3, contracts["whitelist_contract"])
    contracts["csToken_py"] = csTokenRepo.csTokenRepo(w3, contracts["csToken_contract"])
    contracts["ConditionalTokens_py"] = ConditionalTokensRepo.ConditionalTokensRepo(w3, contracts["ConditionalTokens_contract"])
    contracts["lmsrmm_py"] = MarketMakersRepo.MarketMakersRepo(w3, contracts["lmsrmm_contract"])
    contracts["lmsrmmf_py"] = MarketMakersFactoryRepo.MarketMakersFactoryRepo(w3, contracts["lmsrmmf_contract"])
    return contracts

def conf_market(questionId, slotNumber, participants_list, fee=0, ammFunding=30000):
    marketConf = defaultdict(lambda: "Not Present")
    marketConf['slotNumber'] = slotNumber
    marketConf['fee'] = fee
    marketConf['ammFunding'] = ammFunding
    marketConf['questionId'] = questionId
    marketConf['participants'] = participants_list
    return marketConf

    

def activate_market(w3, questionId, slotNumber, participants_list):
    print('DEBUG: configuring market')
    questionId = w3.keccak(questionId)
    marketConf = conf_market(questionId, slotNumber, participants_list)
    print('DEBUG: loading contract')
    contracts = loadContracts(w3)
    CMM = CreateMarketMaker.CreateMarketMaker(w3, contracts)
    lmsrmmConf = CMM.createMM(marketConf, account_admin, private_key, 5000000)
    return lmsrmmConf

def append_whitelist(whitelistPy, newUserList):
    whitelistPy.addToWhitelist(newUserList,account_admin, private_key, 1000000)
    return
    
def close_market(w3, address, abi):
    lmsrMarketMaker_contract = w3.eth.contract(address=address,abi=abi)
    lmsrMarketMaker = MarketMakersRepo.MarketMakersRepo(w3, lmsrMarketMaker_contract)
    tx_receipt = lmsrMarketMaker.close(account_admin, private_key, 1000000)
    return tx_receipt

def report_payout(w3, ConditionalTokens, naiveId, payouts):
    questionId = Web3.toHex(w3.keccak(naiveId))
    # generatedConditionId = ConditionalTokens.getConditionId(account_admin, questionId, 2)
    # print(generatedConditionId)
    print("questionID: {}".format(questionId))
    print("payouts: {}".format(payouts))
    print("Conditional Token address: {}".format(ConditionalTokens.getAddress()))
    tx_receipt = ConditionalTokens.reportPayouts(questionId, payouts, account_admin, private_key, 1000000)
    return tx_receipt

def get_leaderboard(csToken, user_list, user_names):
    d = []
    assert(len(user_list) == len(user_names))
    for i in range(len(user_list)):
        u = user_list[i]
        u_name = user_names[i]
        checksum_u = Web3.toChecksumAddress(u)
        balance = csToken.balanceOf(checksum_u)
        user = User.objects.get(username=u)
        # obj = User_Reputation.objects.get_or_create(user__username=u)
        # try:
        #     obj = User_Reputation.objects.get(user=user)
        # except User_Reputation.DoesNotExist:
        #     obj = User_Reputation(user=user)
        #     obj.save()
        # ups = obj.ups
        # downs = obj.downs
        u_comments = Comment.objects.filter(name=user)
        ups = sum([c.likes.count() for c in u_comments])
        downs = sum([c.dislikes.count() for c in u_comments])
        d.append([u_name, balance, ups, downs])
    leaders = sorted(d, key=lambda x: x[1], reverse=True)
    return leaders

def get_trade_tx_status():
    return 0