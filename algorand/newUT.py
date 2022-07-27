import json
import importlib.resources
from algosdk.future.transaction import LogicSig

from base64 import b64decode, b64encode

pool_logicsig_def = _contracts['contracts']['pool_logicsig']['logic']

validator_app_def = _contracts['contracts']['validator_app']


def get_pool_logicsig(validator_app_id, asset1_id, asset2_id):
    assets = [asset1_id, asset2_id]
    asset_id_1 = max(assets)
    asset_id_2 = min(assets)
    program_bytes = get_program(pool_logicsig_def, variables=dict(
        validator_app_id=validator_app_id,
        asset_id_1=asset_id_1,
        asset_id_2=asset_id_2,
    ))
    return program_bytes
    # return LogicSig(program=program_bytes)

def get_program(definition, variables=None):
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



def encode_value(value, type):
    if type == 'int':
        return encode_varint(value)
    raise Exception('Unsupported value type %s!' % type)


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
