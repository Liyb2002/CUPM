from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View


from web3 import Web3
from web3.middleware import geth_poa_middleware

import json
import os
from django.conf import settings


#Connect Web3
w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/08ef2304798243e6b4dd03945d85e2ac'))
w3.middleware_onion.clear()
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

#Create Faucet Contract Instance
f = open(os.path.join(settings.BASE_DIR, 'app/abi.json'))
ABI = json.load(f)
contract_address='0xc3CD1fE9b0848fF9929F1e2b1879f255231cc89F'
Faucet_instance = w3.eth.contract(contract_address, abi=ABI)

#Create CST Contract Instance
f2 = open(os.path.join(settings.BASE_DIR, 'app/CST.json'))
ABI2 = json.load(f2)
contract_address2='0xb41E0D7463F11D3e772C8B3aD3b9bea6DAb03D62'
CST_instance = w3.eth.contract(contract_address2, abi=ABI2)


#Prepare an account
private_key = "2edb0f009f6a5118cd50e155d3dff0d611479c5717b288877608a0f949ea356a"
acct = w3.eth.account.privateKeyToAccount(private_key)
nonce = w3.eth.get_transaction_count('0x830219365648553C0972543B7ace77403c8E0E26')  
w3.eth.defaultAccount = acct.address

def index(request):
    return HttpResponse(Faucet_instance.address)

class indexPage(View):
    TEMPLATE = 'index.html'
    def get(self, request):
        totalSecs = Faucet_instance.functions.UserToClaim().call()

        if(totalSecs > 86400):
            hours=0
            minutes=0
            seconds=0
            claimed="You haven't claimed yet"
        else:
            hours = int(totalSecs/3600)
            minutes = int((totalSecs - hours*3600)/60)
            seconds = totalSecs%60
            claimed="Please wait for the next bonus claim"
       
        return render(request, self.TEMPLATE,
        {
        "FaucetRemain":Faucet_instance.functions.FaucetAmount().call(),
        "UserAmount":CST_instance.functions.balanceOf('0x830219365648553C0972543B7ace77403c8E0E26').call(),
        "BonusHour":hours,
        "BonusMinute":minutes,
        "BonusSecond":seconds,
        "isClaimed":claimed
        })


def ClaimToken(request):
    print("hi")
    private_key = "2edb0f009f6a5118cd50e155d3dff0d611479c5717b288877608a0f949ea356a"
    acct = w3.eth.account.privateKeyToAccount(private_key)
    nonce = w3.eth.get_transaction_count('0x830219365648553C0972543B7ace77403c8E0E26')  
    #Build TX
    tx_hash = Faucet_instance.functions.claim().buildTransaction({
     'chainId': 4,
     'gas': 70000,
     'maxFeePerGas': w3.toWei('2', 'gwei'),
     'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
     'nonce': nonce,
        })
    signed_txn = w3.eth.account.sign_transaction(tx_hash, private_key=private_key)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)  
    
    if(Faucet_instance.functions.UserToClaim().call()==0):
        return HttpResponse("Claimed 100 CST Tokens!")
    elif (Faucet_instance.functions.UserToClaim().call() > 86400):
        return HttpResponse("Claimed 1000 CST Tokens!")
    else:
        return HttpResponse("Claimed 1 CST Tokens!")