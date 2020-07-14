# Run the script in a computer with oracle libraries
# x2go machines should be fine
import sys
import cx_Oracle
import random
from pprint import pprint

conn_str = u'CMS_ECAL_CONF/0r4cms_3c4lc0nf@cms_tstore'

wgroups = "EcalTPGWeightGroup_perstrip.txt"
wids = "EcalTPGWeightIdMap_perstrip.txt"
logicid_file = "logicids_EBEE.txt"

group_map = {}
weights_values = {}
weights_logicid = {}
logicid_map = {}

with open(logicid_file) as lm: 
    for l in lm.readlines():
        n = l.strip().split(",")
        logicid_map[n[0]] = n[5].strip()


# Make the weights groups unique
# We need to save the position 
with open(wids) as wf:
    nwg = 0
    for i, l in enumerate(wf.readlines()):
        ws = tuple(l.strip().split(" "))
        if ws not in weights_values: 
            weights_values[ws] = nwg
            nwg +=1
        
        group_map[i] = weights_values[ws]

with open(wgroups) as wg:
    for i, l in enumerate(wg.readlines()):
        d = l.strip().split(" ")
        if d[0] not in logicid_map:
            print "Problem! Missing logicid for ",d[0]
            continue
        logicid = logicid_map[d[0]]
        weights_logicid[logicid] = group_map[int(d[1])]

def main(argv):

    conn = cx_Oracle.connect(conn_str)
    c = conn.cursor()

    # Insert a new wei_conf_version
    insert_info_query = u"INSERT into FE_CONFIG_WEIGHT_INFO (wei_conf_id, tag, number_of_groups, db_timestamp) \
            VALUES (FE_CONFIG_WEIGHT_SQ.nextval, 'Test_weights_by_strip', {}, CURRENT_TIMESTAMP) ".format(len(weights_values))
    c.execute(insert_info_query)
    print("N weights", len(weights_values))

    # Now get the wei_conf_version
    # Get last version with tag 'Test_weights_by_strip'
    c.execute("SELECT max(wei_conf_id) from FE_CONFIG_WEIGHT_INFO where Tag='Test_weights_by_strip'")
    for row in c:
        wei_conf_id = row[0]
    print "New weight conf_id: ", wei_conf_id

    # Inserting weight group
    for Ws, groupid in weights_values.items():
        #### NB. Weights order is inverted! From right to left.
        insert_query = u"INSERT into FE_WEIGHT_PER_GROUP_DAT (wei_conf_id, group_id, W4,W3,W2,W1,W0) \
                VALUES ({0}, {1}, {2},{3},{4},{5},{6}) ".format(wei_conf_id, groupid, Ws[0], Ws[1],Ws[2],Ws[3],Ws[4])
        print(insert_query)
        c.execute(insert_query)

   
    # Inserting the logic_id weight _dat
    for lid, groupid in weights_logicid.items():
        insert_query = u"INSERT into FE_CONFIG_WEIGHT_DAT (wei_conf_id, logic_id, group_id) \
                VALUES ({0},{1},{2})".format(wei_conf_id, lid, groupid)
        print(insert_query)
        c.execute(insert_query)

    conn.commit()

    print "\nModification on the DB done."

if __name__ == "__main__":
  main(sys.argv)

