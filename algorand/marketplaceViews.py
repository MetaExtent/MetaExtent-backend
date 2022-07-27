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


def marketplace(request):
        
    nft_marketplace_asc1 = NFTMarketplaceASC1()
    client = getClient()
        
    approval_program_compiled = compileTeal(
        nft_marketplace_asc1.approval_program(),
        mode=Mode.Application,
        version=5,
    )

    clear_program_compiled = compileTeal(
        nft_marketplace_asc1.clear_program(),
        mode=Mode.Application,
        version=5
    )



    approval_program_bytes = NetworkInteraction.compile_program(
        client=client, source_code=approval_program_compiled
    )

    clear_program_bytes = NetworkInteraction.compile_program(
        client=client, source_code=clear_program_compiled
    )

    local_schema = {
        "num_uints" : 0,
        "num_byte_slices" : 0
    }
    global_schema = {
        "num_uints" : 3,
        "num_byte_slices" : 3
    }

 
    
    returnResponse = {
        "approval_program_compiled" : approval_program_compiled,
        "clear_program_compiled"    : clear_program_compiled,
        "local_schema"              : local_schema,
        "global_schema"             : global_schema
    

    }

    return JsonResponse(returnResponse)

def escrow_program(request):
    app_id = int(request.GET['app_id'])
    nft_id = int(request.GET['nft_id'])
    escrow_fund_program_compiled = compileTeal(
        nft_escrow(app_id=app_id, asa_id=nft_id),
        mode=Mode.Signature,
        version=4,
    )

    nft_marketplace_asc1 = NFTMarketplaceASC1()
    client = getClient()
    compiledProgram = NetworkInteraction.compile_program(
        client=client, source_code=escrow_fund_program_compiled
    )

   
    escrow_address = algo_logic.address(compiledProgram)
    print(escrow_address)
    returnResponse ={
        "escrow_fund_program_compiled" : escrow_fund_program_compiled,
        "initialize_escrow" :nft_marketplace_asc1.AppMethods.initialize_escrow,
        "escrow_address" : escrow_address
    }
    return JsonResponse(returnResponse)

def pending_transaction_info(request):
    tx_id = request.GET['tx_id']
    client =getClient()
    transaction_response = client.pending_transaction_info(tx_id)
    return JsonResponse({
        "transaction_response" : transaction_response
    })

def decodeAddress(request):
    addr1 = decode_address(request.GET['address1'])
    addr2 = decode_address(request.GET['address2'])
    print(addr1)
    return JsonResponse({"address1":"ok","address2":"ok"})

def logicSigInfo(request):
    app_id = int(request.GET['app_id'])
    nft_id = int(request.GET['nft_id'])
    client = getClient()
    escrow_fund_program_compiled = compileTeal(
            nft_escrow(app_id=app_id, asa_id=nft_id),
            mode=Mode.Signature,
            version=4,
     )



    escrow_bytes = NetworkInteraction.compile_program(
    client=client, source_code=escrow_fund_program_compiled
    )

    
    asa_transfer_txn_logic_signature = algo_txn.LogicSig(escrow_bytes)
   
    # byteCode =  list(b64decode(asa_transfer_txn_logic_signature))
    # print(algo_logic.address(asa_transfer_txn_logic_signature))
    return JsonResponse({"ok":"ok"})


def getClient():
    
    address = "https://testnet-algorand.api.purestake.io/ps2"
    token   = ""
    purestake_token = {
        "X-API-Key": "1nYJyGUcqI4QNR7ChogoU2839CD3Osh7a6EVEBtv",
    }

    algod_client = algod.AlgodClient(token, address, headers=purestake_token)
    
    return algod_client