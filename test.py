# coding=utf-8
import GeniusFramework
import sys
contract_name = "tea"
id_type = "bytes32" 
schema = "string name,string color,string description,string data,string hash"
ipfshash = "QmTWMxKvnu5EMwQoweHvAmaMxmxW1HGv6ar6r28zHzrZRY"

a = GeniusFramework.GeniusFramework()

#print(a.deploy(contract_name, id_type, schema))

#Dresult = a.DownloadContractInfo(ipfshash)
#if Dresult['status']!='SUCCESS':
#    exit(Dresult['result'])

Lresult = a.LoadContractInfo()
if Lresult['status']=='SUCCESS':
    #print(a.SetInfo('id01','green tea','red','haha','中文','fhash'))
    print(a.GetInfo('id01',schema))
else:
    print(Lresult['result'])

