import os 
import sys
import cx_Oracle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputfile",  type=str, help="Input parameters file", required=True)
parser.add_argument("-o", "--outputfile",  type=str, help="Output file", required=True)
parser.add_argument("-s", "--subdet",  type=str, help="Subdetector EB/EE", required=True)
parser.add_argument("-p","--password", type=str, help="ConfDB password", required=True)
args = parser.parse_args()

conn_str = u'CMS_ECAL_CONF/{}@cms_tstore'.format(args.password)

strips = []
with open(args.inputfile) as file:
    for l in file.readlines()[1:]:
        if l.startswith("#"): continue
        strips.append(list(map(int, l.split(","))) )



if args.subdet == "EB":
        
    conn = cx_Oracle.connect(conn_str)
    c = conn.cursor()

    query = "SELECT ID1,ID2,ID3,logic_id from channelview where  NAME='ECAL_readout_strip' and MAPS_TO='EB_VFE'"
    c.execute(query)

    logid = {}
    for row in c:
        logid[(row[0], row[1], row[2])] = row[3]

    
    for strip in strips :
        strip.append(logid[(strip[2], strip[3], strip[4])])

    with open(args.outputfile, "w") as of:
        of.write("stripid,cmsswid,FED,TT,VFE,logicid\n")
        for strip in strips:
            of.write(",".join(map(str,strip)) +"\n")


elif args.subdet == "EE":
  
    conn = cx_Oracle.connect(conn_str)
    c = conn.cursor()

    query = "SELECT ID1,ID2,ID3,logic_id from channelview where  NAME='ECAL_readout_strip' and MAPS_TO='ECAL_readout_strip'"
    c.execute(query)

    logid = {}
    for row in c:
        logid[(row[0], row[1], row[2])] = row[3]

    
    for strip in strips :
        strip.append(logid[(strip[2], strip[3], strip[4])])

    with open(args.outputfile, "w") as of:
        of.write("stripid,cmsswid,FED,CCU,VFE,logicid\n")
        for strip in strips:
            of.write(",".join(map(str,strip)) +"\n")


else:
  print("Please specify --subdet EE/EB")
  exit(1)
