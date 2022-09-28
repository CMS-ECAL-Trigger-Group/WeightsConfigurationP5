# Run the script in a computer with oracle libraries
# x2go machines should be fine
from __future__ import print_function
import sys
import cx_Oracle
import random
from pprint import pprint
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--weight-config", type=str, help="Weight config id", required=True)
parser.add_argument("-wt", "--weight-type", type=str, help="Weight type [even/odd]", required=True)
parser.add_argument("-l","--logicid", help="Logicid mapping", default="params_EBEE_logicid.csv")
parser.add_argument("-o","--outputname", help="Name for the output files", required=True)
parser.add_argument("-p","--password", type=str, help="ConfDB password", required=True)
args = parser.parse_args()

if args.weight_type == "even":
    weight_table = "WEIGHT"
    confid_col = "wei_conf_id"
elif args.weight_type == "odd":
    weight_table = "WEIGHT2"
    confid_col = "wei2_conf_id"
else:
    print("Please specify the Weight type even/odd")
    exit(1)


conn_str = u'CMS_ECAL_CONF/{}@cms_tstore'.format(args.password)

weights_groups = []
weights_map = {}
logicid_map = {}

with open(args.logicid) as lm: 
    for l in lm.readlines()[1:]:
        n = l.strip().split(",")
        logicid_map[n[5].strip()] = n[0]


conn = cx_Oracle.connect(conn_str)
c = conn.cursor()

#General info
c.execute("SELECT NUMBER_OF_GROUPS, DB_TIMESTAMP, TAG from FE_CONFIG_{}_INFO where {}={}".format(
    weight_table, confid_col, args.weight_config))

print("Info for Weight config: ", args.weight_config)
for row in c:
    print("Tag:", row[2])
    print("Created on: ", row[1])
    print("Number of groups", row[0])
    

# TP mode info
if args.weight_type == "odd":
    print("###################################")
    print("TP MODE flags")
    c.execute("SELECT * FROM FE_WEIGHT2_MODE_DAT WHERE WEI2_CONF_ID={}".format(args.weight_config))
    for row in c:
        print("\tEnable EB Odd filter ", row[1])
        print("\tEnable EE Odd filter ", row[2])
        print("\tEnable EB Odd Peak finder ", row[3])
        print("\tEnable EE Odd Peak finder ", row[4])
        print("\tDisable EB Even peak finder ", row[5])
        print("\tDisable EE Even peak finder ", row[6])
        print("\tFenix EB Strip output ", row[7], "  # 0=even, 1=odd, 2=larger, 3=sum")
        print("\tFenix EE Strip output ", row[8], "  # 0=even, 1=odd, 2=larger, 3=sum")
        print("\tFedix EB Strip infobit2 ", row[9], "  #odd>event strip flag")
        print("\tFenix EE Strip infobit2 ", row[10], " #odd>event strip flag")
        print("\tFenix EB TCP Output ", row[11], "  # 0=even sum, 1=larger, 2=even+odd sum" )
        print("\tFenix EB TCP infobit1 ", row[12], " #0=FGVB, 1=odd>even TCP sum")
        print("\tFenix EE TCP Output ", row[13], "  # 0=even sum, 1=larger, 2=even+odd sum" )
        print("\tFenix EE TCP infobit1 ", row[14], " #0=FGVB, 1=odd>even TCP sum")

print("#############################")
print("Weights infos")
        
# Query weight group
_query = u"SELECT group_id, W4,W3,W2,W1,W0 from FE_{}_PER_GROUP_DAT where {}={}".format(
        weight_table, confid_col, args.weight_config)

c.execute(_query)
gfile = open("EcalTPGWeightGroup_"+args.outputname + ".txt","w")
for row in c:
    weights = list(row[1:])
    weights[3] -= 128 # remove the 8th bit from the 4th weight
    print("Group ID: {}, Weights: {},{},{},{},{}".format(row[0], *weights))
    gfile.write("{} {} {} {} {}\n".format(*weights))
gfile.close()

# Query the ID map
_query = u"SELECT logic_id, group_id from FE_CONFIG_{}_DAT where {}={}".format(
    weight_table, confid_col, args.weight_config)

c.execute(_query)
print("Querying the mapping and saving to file")
gfile = open("EcalTPGWeightIdMap_"+args.outputname + ".txt","w")
for row in c:
    stripid = logicid_map[str(row[0])]
    gfile.write("{} {}\n".format(stripid, row[1] ))
gfile.close()

print("DONE")    


