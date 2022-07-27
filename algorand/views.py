from os import access
from urllib import response
from xml.etree.ElementInclude import include
from django.shortcuts import render
from django.http import HttpResponse
from .swappingTest import swapping
from .optin import prepare_app_optin_transactions,optInSubmit
from .client import clientInfo,algodClientInfo
from django.http import JsonResponse
from base64 import b64decode, b64encode
from algosdk.future.transaction import LogicSigTransaction, assign_group_id
from algosdk.error import AlgodHTTPError

from algosdk.mnemonic import to_private_key

import json

from algosdk.transaction import AssetConfigTxn

from algosdk.future.transaction import LogicSig
from base64 import b64decode, b64encode
import algosdk
import importlib.resources
# Create your views here.
from .newUT import get_pool_logicsig

from decouple import config



def index(request):

    address          = request.GET['address']
    private          = request.GET['private']
    private          = to_private_key(private)
    asset1           = int(request.GET['asset1'])
    asset2           = int(request.GET['asset2'])

    client           = clientInfo(address)
    asset1           = client.fetch_asset(asset1)
    asset2           = client.fetch_asset(asset2)
    pool             = client.fetch_pool(asset1, asset2)

    asset_2_amount   = int(request.GET['asset_2_amount'])



    returnString = {""}

    print("slippage tolerance:")
    print(quote.price_with_slippage)
    if quote.price_with_slippage > 0:
        print(f'Swapping {quote.amount_in} to {quote.amount_out_with_slippage}')
        # Prepare a transaction group
        transaction_group = pool.prepare_swap_transactions_from_quote(quote)
        
       
       
       
        # Sign the group with our key
       

        transaction_group.sign_with_private_key(address, private)
        # Submit transactions to the network and wait for confirmation
       
        result1 = client.submit(transaction_group, wait=True)

        # Check if any excess remaining after the swap
        excess = pool.fetch_excess_amounts()
        if asset1 in excess:
            amount = excess[asset1]
            print(f'Excess: {amount}')
            if amount > asset_2_amount:
                transaction_group = pool.prepare_redeem_transactions(amount)
                transaction_group.sign_with_private_key(address, private)
                result = client.submit(transaction_group, wait=True)
 
 
    return HttpResponse({"returnvalue" :"success"})


def swapInfo(request):
    address          = request.GET['address']
    # private          = request.GET['private']
    # private          = to_private_key(private)
    asset1           = int(request.GET['asset1'])
    asset2           = int(request.GET['asset2'])

    client           = clientInfo(address)
    asset1           = client.fetch_asset(asset1)
    asset2           = client.fetch_asset(asset2)
    pool             = client.fetch_pool(asset1, asset2)

    asset_2_amount   = int(request.GET['asset_2_amount'])


    quote = pool.fetch_fixed_input_swap_quote(asset2(asset_2_amount), slippage=0.01)
    print(dir(quote))


    print(f'ASEET IN: {quote.amount_in}')
    print(f'ASEET IN ID: {quote.amount_in.asset.id}')
    print(f'ASEET out: {quote.amount_out}')
    print(f'ASEET out ID: {quote.amount_out.asset.id}')


    returnString = {""}


    
    

    return JsonResponse({'quote' : 'success'})

def optin(request):
    
    address          = request.GET['address']
    # validator_app_id = 62368684
    client           = clientInfo(address)
    algodClient      = algodClientInfo()
    suggestedParams  = algodClient.suggested_params()

   
    returnValue = prepare_app_optin_transactions(validator_app_id,address,suggestedParams)
    print(validator_app_id)
  
    signResult  = returnValue.sign_with_private_key("RRO7OHROIWSOA7YXJBACWXOTCG4BWX3XLNSJLTJUSPRI5KHP3JXUTDM63Q","2EAowHTBIec7v4825qYqczCTp+3vgWQ0HqzxvVXfYWaMXfceLkWk4H8XSEArXdMRuBtfd1tklc00k+KOqO/abw==")
    print(signResult)
    #signResult  = returnValue.sign(client)
    #submitResult = wait_for_confirmation(algodClient,"BBLAM3BD5CNYEMO2PCT4VKUZ2O7KDJYEJPC3QRAZLNAY5NUZ7E4Q")

    # checkOptinSubmit = optInSubmit(algodClient,"RNQZGBWBQETGVMJZKFHOYED5C3BN6ZSZR3Q5JHSFYQPCBTZK7ODA")
    
    

    return HttpResponse("Success")


def checkOptin(request):
    address          = request.GET['address']
    client           = clientInfo(address)
    optinInResult    = client.is_opted_in()
    algodClient      = algodClientInfo()
    algodClientInfos = algodClient.account_info(address)

   

    responseData     = {
        "optinInResult" : optinInResult,
        "clientInfo"    : algodClientInfos
      
    }
    return JsonResponse(responseData)

def checkAssetOptin(request):
    address          = request.GET['address']
    assetId          = int(request.GET['assetId'])
    
    client           = clientInfo(address)
    algodClient      = algodClientInfo()

    try:

        optinInResult    = client.asset_is_opted_in(assetId,address)
        responseData     = {
          "optinInResult" : optinInResult,        
        }
        
       
        return JsonResponse(responseData)
       
    except NameError:
         return JsonResponse({"error" : "Error Exception"})

def accountInfo(request):
    address          = request.GET['address']
    algodClient      = algodClientInfo()
    algodClientInfos = algodClient.account_info(address)

   

    responseData     = {
       
        "clientInfo"    : algodClientInfos
      
    }
    return JsonResponse(responseData)



def createAsset(request):
    # CREATE ASSET
    # Get network params for transactions before every transaction.
    algodClient      = algodClientInfo()
    params  = algodClient.suggested_params()

   
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    # Account 1 creates an asset called latinum and
    # sets Account 2 as the manager, reserve, freeze, and clawback address.
    # Asset Creation transaction

    
    txn = AssetConfigTxn(
        sender="XQUXRUK2XUNJDT22J5BKYUADZHRWE5K5R5M23SNYINHPUYXCE42V3OO27I",
        fee=params.fee,
        first=params.first,
        last=params.last,
        gh = params.gh,
        total=1000000,
        default_frozen=False,
        unit_name="PAGO",
        asset_name="PAGO",
        manager="XQUXRUK2XUNJDT22J5BKYUADZHRWE5K5R5M23SNYINHPUYXCE42V3OO27I",
        reserve="XQUXRUK2XUNJDT22J5BKYUADZHRWE5K5R5M23SNYINHPUYXCE42V3OO27I",
        freeze="XQUXRUK2XUNJDT22J5BKYUADZHRWE5K5R5M23SNYINHPUYXCE42V3OO27I",
        clawback="XQUXRUK2XUNJDT22J5BKYUADZHRWE5K5R5M23SNYINHPUYXCE42V3OO27I",
        url="https://path/to/my/asset/details", 
        decimals=0)

    # Sign with secret key of creator
    stxn = txn.sign("L30zWF9sGjtXJ4ugx8SOWKr92Gb036mTze+gk55deXu8KXjRWr0akc9aT0KsUAPJ42J1XY9Zrcm4Q076YuInNQ==")
    
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algodClient.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algodClient, txid)  
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))   
        print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    except Exception as err:
        print(err)
    # Retrieve the asset ID of the newly created asset by first
    # ensuring that the creation transaction was confirmed,
    # then grabbing the asset id from the transaction.
    
    # print("Decoded note: {}".format(base64.b64decode(
    #     confirmed_txn["txn"]["txn"]["note"]).decode()))
    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk'])
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algodClient.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]

        print(asset_id)
        # print_created_asset(algod_client, accounts[1]['pk'], asset_id)
        # print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
    except Exception as e:
        print(e)
    return 0

def showPK(request):
    private = request.GET['private']
    private_key = to_private_key(private)
    return JsonResponse({"result": private_key})


def createPool(request):

    address          = request.GET['address']
    asset1_id        = request.GET['asset1_id']
    asset2_id        = request.GET['asset2_id']

    client           = clientInfo(address)
    # Fetch our two assets of interest
    # ALGO = Asset(id=0, name='Algo', unit_name='ALGO', decimals=6)

    # Create the pool we will work with and fetch its on-chain state
    pool = Pool(client, int(asset1_id), int(asset2_id), fetch=True,validator_app_id=validator_app_id)
   # pool = client.fetch_pool(91875594,0)
    #poolInfo = pool.info()

    

    return JsonResponse({"pool_address":pool.address})


def addLiquidity(request):
    
    # Fetch our two assets of interest
    address          = request.GET['address']
    pk               = request.GET['pk']

    client           = clientInfo(address)
    ALGO             = client.fetch_asset(0)
   
    # Check if we are happy with the quote..
    if quote.amounts_in[ALGO] < 5_000_000:
        # Prepare the mint transactions from the quote and sign them
        transaction_group = pool.prepare_mint_transactions_from_quote(quote)
        transaction_group.sign_with_private_key(address,'L30zWF9sGjtXJ4ugx8SOWKr92Gb036mTze+gk55deXu8KXjRWr0akc9aT0KsUAPJ42J1XY9Zrcm4Q076YuInNQ==')
        result = client.submit(transaction_group, wait=True)

       # print(quote.amounts_in)
        print(quote.liquidity_asset_amount_with_slippage)
       
        return JsonResponse({"ok":"ok"})

       

        

        # Check if any excess liquidity asset remaining after the mint
        excess = pool.fetch_excess_amounts()
        # if pool.liquidity_asset in excess:
        #     amount = excess[pool.liquidity_asset]
        #     print(f'Excess: {amount}')
        #     if amount > 1_000_000:
        #         transaction_group = pool.prepare_redeem_transactions(amount)
        #         transaction_group.sign_with_private_key(address,pk)
        #         result = client.submit(transaction_group, wait=True)

    info = pool.fetch_pool_position()
    share = info['share'] * 100
    print(f'Pool Tokens: {info[pool.liquidity_asset]}')
    print(f'Share of pool: {share:.3f}%')


def getProgramByte(request):

    # print(request.body.decode('utf-8'))
    
    body_unicode = request.body.decode('utf-8') 	
    body = json.loads(body_unicode) 	
    # content = body['content']
    pool_logicsig_def = body['main']
    variables=dict(
        validator_app_id=body['validator_app_id'],
        asset_id_1=body['asset_id_1'],
        asset_id_2=body['asset_id_2']
    )
    swap_types = {
        'fixed-input': 'fi',
        'fixed-output': 'fo',
    }
    print(['swap', swap_types['fixed-input']])
    byteInfo = get_program2(pool_logicsig_def,variables)
    
    
    return JsonResponse({"byteInfo":byteInfo})


def get_program2(definition, variables=None):
    """
    Return a byte array to be used in LogicSig.
    """
    template = definition['bytecode']
    template_bytes = list(b64decode(template))
   
   
    offset = 0
    for v in sorted(definition['variables'], key=lambda v: v['index']):
        name = v['name'].split('TMPL_')[-1].lower()
        value = variables[name]
        start = v['index'] - offset
        end = start + v['length']
        value_encoded = encode_value(value, v['type'])
        value_encoded_len = len(value_encoded)
        diff = v['length'] - value_encoded_len
        offset += diff
        template_bytes[start:end] = list(value_encoded)
        
    return template_bytes
    # return bytes(template_bytes)

def encode_value(value, type):
    if type == 'int':
        return encode_varint(value)
    # raise Exception('Unsupported value type %s!' % type)


def encode_varint(number):
    buf = b''
    while True:
        towrite = number & 0x7f
        number >>= 7
        if number:
            buf += bytes([towrite | 0x80])
        else:
            buf += bytes([towrite])
            break
    return buf

def bootstrapInfo(request):

    byteInfo = get_pool_logicsig(62368684,int(request.GET['asset1']),int(request.GET['asset2']))
        
    return JsonResponse({"byteInfo":byteInfo})


def poolInfo(request):
    address          = request.GET['address']
    asset1           = int(request.GET['asset1'])
    asset2           = int(request.GET['asset2'])
   
    client           = clientInfo(address)
    asset1           = client.fetch_asset(asset1)
    asset2           = client.fetch_asset(asset2)
    asset2_amount    = int(request.GET['asset2_amount'])

    # Fetch the pool we will work with
    
    pool = client.fetch_pool(asset1, asset2)
  
    poolInfo = pool.info()
    

    quote = pool.fetch_fixed_input_swap_quote(asset2(1_000_000 * asset2_amount), slippage=0.01)
    # quote2 = pool.fetch_mint_quote(asset2(1000_000_000), slippage=0.01)
    
    
    # print(quote2)
    # print(quote)

    # # swapQuote = pool.fetch_fixed_input_swap_quote(asset1)
    # print(quote)
    
    # # poolInfo

    ###############################################################################################

        # print(request.body.decode('utf-8'))

    # pool_logicsig_def = _contracts['contracts']['pool_logicsig']['logic']
    # variables=dict(
    #     validator_app_id=62368684,
    #     asset_id_1=asset1,
    #     asset_id_2=asset2
    # )
    # swap_types = {
    #     'fixed-input': 'fi',
    #     'fixed-output': 'fo',
    # }
  
    # byteInfo = get_programF(pool_logicsig_def,variables)
    byteInfo = get_pool_logicsig(62368684,int(request.GET['asset1']),int(request.GET['asset2']))
    
   
    # print(dir(ls))
    
    
    if(int(request.GET['asset1']) == 92772865):
        print("halelola")
        quote_price = quote.price*1000000
        quote_price_with_slippage = quote.price_with_slippage*1000000
    else:
        quote_price = quote.price
        quote_price_with_slippage = quote.price_with_slippage
    print("hello world")
  
    returnResponse = {
        "pool_info" : poolInfo,
        "asset_in_id":quote.amount_in.asset.id,
        "asset_out_id":quote.amount_out.asset.id,
        "asset_in_amount":quote.amount_in.amount,
        "asset_out_amount":quote.amount_out.amount,
        "Asset2_price_perAsset1" :quote_price*asset2_amount,
        "Asset2_price_perAsset1_worst_case" :quote_price_with_slippage*asset2_amount,
        "byteInfo" : byteInfo
    }
    return JsonResponse(returnResponse)