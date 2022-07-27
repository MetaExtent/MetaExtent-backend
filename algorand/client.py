from pydoc import cli
from algosdk.v2client import algod
from decouple import config

validator_app_id  = config('tinyman_validator_app_id')
algod_address_c  = config('algod_address')
algod_token_c  = config('algod_token')

algod_address = algod_address_c
algod_token = algod_token_c
headers = {
    "X-API-Key": algod_token,
}


algod_client = algod.AlgodClient(algod_token, algod_address, headers)


def clientInfo(address):

    client = Client(
        algod_client=algod_client,
        _app_id=ID,
        user_address = address
    )
    
    return client

def algodClientInfo():
    return algod_client




