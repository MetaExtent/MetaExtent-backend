import base64
import algosdk
from algosdk.future.transaction import ApplicationOptInTxn, AssetOptInTxn
from algosdk.v2client.algod import AlgodClient


from algosdk.v2client import algod

def prepare_app_optin_transactions(validator_app_id, sender, suggested_params):
    txn = ApplicationOptInTxn(
        sender=sender,
        sp=suggested_params,
        index=validator_app_id,
    )
    txn_group = TransactionGroup([txn])
    return txn_group


def prepare_asset_optin_transactions(asset_id, sender, suggested_params):
    txn = AssetOptInTxn(
        sender=sender,
        sp=suggested_params,
        index=asset_id,
    )
    txn_group = TransactionGroup([txn])
    return txn_group


def optInSubmit(client,txid):
    confirmation = wait_for_confirmation(client,txid)



# private_key  = algosdk.mnemonic.to_private_key("brand patient gas blanket drum what what moral short oppose next already chapter hazard legal limit milk juice stock tenant problem jelly credit about quit")
#2EAowHTBIec7v4825qYqczCTp+3vgWQ0HqzxvVXfYWaMXfceLkWk4H8XSEArXdMRuBtfd1tklc00k+KOqO/abw==

