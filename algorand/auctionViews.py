from django.http import JsonResponse
from pyteal import compileTeal, Mode

from algorand import client
from .smart_contracts import NFTMarketplaceASC1, nft_escrow
from algosdk.v2client import algod
from algorand.services.network_interaction import NetworkInteraction
from algosdk.encoding import decode_address
from algosdk import logic as algo_logic
from base64 import b64decode, b64encode
from algosdk.future import transaction as algo_txn

from .smart_contracts.auction import approval_program,clear_state_program


def auctionProgram(request):
        
    nft_marketplace_asc1 = NFTMarketplaceASC1()
    client = getClient()
        

    approval_program_compiled = compileTeal(
        approval_program(),
        mode=Mode.Application,
        version=5,
    )

    clear_program_compiled = compileTeal(
        clear_state_program(),
        mode=Mode.Application,
        version=5
    )


    local_schema = {
        "num_uints" : 0,
        "num_byte_slices" : 0
    }
    global_schema = {
        "num_uints" : 7,
        "num_byte_slices" : 7
    }

 
    
    returnResponse = {
        "approval_program_compiled" : approval_program_compiled,
        "clear_program_compiled"    : clear_program_compiled,
        "local_schema"              : local_schema,
        "global_schema"             : global_schema
    

    }

    return JsonResponse(returnResponse)


def getClient():
    
    address = "https://testnet-algorand.api.purestake.io/ps2"
    token   = ""
    purestake_token = {
        "X-API-Key": "1nYJyGUcqI4QNR7ChogoU2839CD3Osh7a6EVEBtv",
    }

    algod_client = algod.AlgodClient(token, address, headers=purestake_token)
    
    return algod_client