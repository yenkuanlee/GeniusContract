import io
import ipfsapi
import json
import os
from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.middleware import geth_poa_middleware
from solc import compile_source
from web3.contract import ConciseContract
from ethereum.abi import (
    decode_abi,
    normalize_name as normalize_abi_method_name,
    method_id as get_abi_method_id)
from ethereum.utils import encode_int, zpad, decode_hex

IPFS_IP = '127.0.0.1'
IPFS_PORT = '5001'
Cpath = os.path.dirname(os.path.realpath(__file__))
api = ipfsapi.connect(IPFS_IP,IPFS_PORT)

class GeniusFramework:
    def __init__(self):
        self.host = '172.16.0.125'
        self.account = '0xa17806a04439e3e931dd980dd45ca0f5a591a353'
        self.passwd = 'ntuChain'
        self.w3 = Web3(HTTPProvider('http://'+self.host+':3000'))
        self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
        self.account = self.w3.toChecksumAddress(self.account)
        self.abi = ""
        self.contract_instance = ""

    def GenContract(self,contract_name, id_type, schema):
        Sdict = dict() # filed => type
        tmp = schema.split(",")
        for x in tmp:
            Sdict[x.split(" ")[1]] = x.split(" ")[0]
        # Solidity Version    
        contract = "pragma solidity ^0.4.0;\n"
        # Class Name
        contract += "contract "+contract_name.upper()+" {\n"
        # Constructor
        contract += "\tfunction "+contract_name.upper()+"() public{}\n"
        # Ledger Schema
        contract += "\tstruct "+contract_name.lower()+" {\n"
        for x in tmp:
            contract += "\t\t"+x+";\n"
        contract += "\t}\n"
        # User Mapping
        contract += "\tmapping("+id_type+" => "+contract_name.lower()+") public Mapping;\n"
        # Set User Data
        contract += "\tfunction SetInfo("+id_type+" iid,"+schema+"){\n"
        for x in Sdict:
            contract += "\t\tMapping[iid]."+x+" = "+x+";\n"
        contract += "\t}\n"
        # Get User Info
        TypeString = ""
        for x in tmp:
            TypeString += x.split(" ")[0]+","
        TypeString = TypeString[:-1]
        contract += "\tfunction GetInfo("+id_type+" iid)public returns ("+TypeString+"){\n"
        FieldString = ""
        for x in tmp:
            FieldString += "Mapping[iid]."+x.split(" ")[1]+","
        FieldString = FieldString[:-1]
        contract += "\t\treturn ("+FieldString+");\n\t}\n"
        contract += "}"
        return contract

    def deploy(self,contract_name,id_type,schema):
        contract_source_code = self.GenContract(contract_name,id_type,schema)
        compiled_sol = compile_source(contract_source_code)
        contract_interface = compiled_sol['<stdin>:'+contract_name.upper()]
        self.w3.personal.unlockAccount(self.account, self.passwd)
        contractt = self.w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
        tx_hash = contractt.deploy(transaction={'from': self.account, 'gas': 4000000})
        self.w3.eth.waitForTransactionReceipt(tx_hash)
        tx_receipt = self.w3.eth.getTransactionReceipt(tx_hash)
        contract_address = tx_receipt['contractAddress']
        contract_instance = self.w3.eth.contract(abi=contract_interface['abi'], address=contract_address)
        Joutput = dict()
        fw = open(Cpath+'/contract.json','w')
        Joutput['abi'] = contract_interface['abi']
        Joutput['contract_address'] = contract_address
        fw.write(json.dumps(Joutput))
        fw.close()
        ipfshash = api.add(Cpath+'/contract.json')
        Joutput['ipfs_hash'] = ipfshash
        return Joutput

    def DownloadContractInfo(self,ipfshash):
        try:
            api.get(ipfshash)
            os.system("mv "+Cpath+"/"+ipfshash+" "+Cpath+"/contract.json")
            return {"status":"SUCCESS","result":"Download Contract Information Success."}
        except:
            return {"status":"ERROR","result":"Download Contract Information Failed."}

    def LoadContractInfo(self):
        try:
            f = open(Cpath+'/contract.json','r')
            Jline = json.loads(f.readline())
            f.close()
            self.abi = Jline['abi']
            contract_address = Jline['contract_address']
            self.contract_instance = self.w3.eth.contract(abi=self.abi, address=contract_address)
            return {"status":"SUCCESS"}
        except:
            return {"status":"ERROR", "result":"Please download contract information or deploy a new contract."}

    def SetInfo(self,*arg):
        try:
            iid = (self.w3.toBytes(text=arg[0]))
            a = (iid,*arg[1:])
            self.w3.personal.unlockAccount(self.account,self.passwd)
            self.contract_instance.functions.SetInfo(*a).transact({'from': self.account})
            return {"status":"SUCCESS"}
        except Exception as e:
            return {"status":"ERROR","log":str(e),"result":"Set Information Failed."}

    def GetInfo(self,iid):
        iid = (self.w3.toBytes(text=iid))
        result = self.contract_instance.functions.GetInfo(iid).call()
        Odict = dict()
        Odict['name'] = result[0]
        Odict['color'] = result[1]
        Odict['description'] = result[2]
        Odict['date'] = result[3]
        return Odict
