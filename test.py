import GeniusFramework
import sys
contract_name = "tea"
id_type = "bytes32" 
schema = "string name,string color,string description,string data"
ipfshash = "QmZVchHd21PihDn4RaLUiCZcUt8J5UzGDkhhdFytufk1XR"

a = GeniusFramework.GeniusFramework()

#print(a.deploy(contract_name, id_type, schema))

#Dresult = a.DownloadContractInfo(ipfshash)
#if Dresult['status']!='SUCCESS':
#    exit(Dresult['result'])

Lresult = a.LoadContractInfo()
if Lresult['status']=='SUCCESS':
    #print(a.SetInfo('a','b','c','d','e'))
    print(a.GetInfo('a'))
else:
    print(Lresult['result'])

