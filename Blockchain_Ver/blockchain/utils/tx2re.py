import math
from decimal import *

def transaction2receipt(w3, transaction, tx_account, tx_key, appropriate_gas_amount):
    # since a raw transaction might not contain gas & nonce amounts, so you have to add them manually.
    transaction.update({ 'from' : tx_account })
    transaction.update({ 'nonce' : w3.eth.get_transaction_count(w3.toChecksumAddress(tx_account)) })
    transaction.update({ 'gas' : appropriate_gas_amount })
    # (2) sign_transaction
    signed_tx = w3.eth.account.sign_transaction(transaction, tx_key)
    # (3) send raw transaction and wait_for transaction_receipt
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Here is the tx hash: {tx_hash.hex()}")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("\nWas transaction successful?")
    print(tx_receipt["status"])
    return tx_receipt

def prob2pct(probability):
    return round(Decimal(probability)/Decimal(math.pow(2, 64))*100,2)
