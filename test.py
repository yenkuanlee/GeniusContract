# coding=utf-8
import hashlib
import GeniusFramework
import sys
import sqlite3
import os
Cpath = os.path.dirname(os.path.realpath(__file__))

contract_name = "tea"
id_type = "bytes32" 
schema = "string date,string Dtype,string content,string person,string tool,string amount,string dbhash"
ipfshash = "QmR5uuu2x5nzJ9Xn9kaK7en8AUMoRuYRZBu2Z9SwhdUmcj"

a = GeniusFramework.GeniusFramework()

if sys.argv[1]=='deploy':
    print(a.deploy(contract_name, id_type, schema))

elif sys.argv[1]=='download':
    Dresult = a.DownloadContractInfo(ipfshash)
    if Dresult['status']!='SUCCESS':
        exit(Dresult['result'])

elif sys.argv[1]=='set_info':
    tid = sys.argv[2]
    Lresult = a.LoadContractInfo()
    if Lresult['status']=='SUCCESS':
        conn = sqlite3.connect(Cpath+'/data.db')
        c = conn.cursor()
        c.execute("SELECT tid,Ddate,Dtype,content,person,tool,amount FROM "+contract_name+" WHERE TID = 'A001';")
        for x in c:
            m = hashlib.md5()
            m.update(str(x).encode('utf-8'))
            h = m.hexdigest()
            print(a.SetInfo(*x,h))
            break
    else:
        print(Lresult['result'])

elif sys.argv[1]=='get_info':
    tid = sys.argv[2]
    Lresult = a.LoadContractInfo()
    if Lresult['status']=='SUCCESS':
        print(a.GetInfo(tid,schema))
    else:
        print(Lresult['result'])

elif sys.argv[1]=='get_dbhash':
    print(a.GetDBhash(contract_name,sys.argv[2]))
