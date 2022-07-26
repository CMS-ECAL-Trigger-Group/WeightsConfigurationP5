# Run the script in a computer with oracle libraries
# x2go machines should be fine
import sys
import cx_Oracle
import random
from pprint import pprint
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dry", action="store_true", help="Dry run")
parser.add_argument("-t", "--tag", type=str, help="Tag", required=True)
parser.add_argument("--wg",  type=str, help="Weight group file", required=True)
parser.add_argument("--wi",  type=str, help="Weight ID map", required=True)
parser.add_argument("--wt", "--weight-type", type=str, help="Weight type [even/odd]", required=True, default="even")
parser.add_argument("-l","--logicid", help="Logicid mapping", default="params_EBEE_logicid.csv")
parser.add_argument("-p","--password", type=str, help="ConfDB password", required=True)
args = parser.parse_args()
tag= args.tag


if args.weight_type == "even":
    weight_table = "WEIGHT"
elif args.weight_type == "odd":
    weight_table = "WEIGHT2"
else:
    print("Please specify the Weight type even/odd")
    exit(1)

conn_str = u'CMS_ECAL_CONF/{}@cms_tstore'.format(args.password)

wgroups = args.wg
wids = args.wi
logicid_file = args.logicid

weights_values = []
weights_logicid = {}
logicid_map = {}

with open(logicid_file) as lm: 
    for l in lm.readlines()[1:]:
        n = l.strip().split(",")
        logicid_map[n[0]] = n[5].strip()

# Make the weights groups unique
# We need to save the position 
with open(wgroups) as wf:
    for l in wf:
        ws = tuple(l.strip().split(" "))
        weights_values.append(ws)
         
with open(wids) as wg:
    for l in wg:
        d = l.strip().split(" ")
        if d[0] not in logicid_map:
            print "Problem! Missing logicid for ",d[0]
            continue
        logicid = logicid_map[d[0]]
        weights_logicid[logicid] = int(d[1])

def main(argv):

    conn = cx_Oracle.connect(conn_str)
    c = conn.cursor()

    # Insert a new wei_conf_version
    insert_info_query = u"INSERT into FE_CONFIG_{}_INFO (wei_conf_id, tag, number_of_groups, db_timestamp) VALUES\
                     (FE_CONFIG_WEIGHT_SQ.nextval, '{}', {}, CURRENT_TIMESTAMP)".format(weight_table, tag, len(weights_values))
    print"QUERY: ", insert_info_query
    if not args.dry: c.execute(insert_info_query)
    print"N weights", len(weights_values)

    # Now get the wei_conf_version
    # Get last version with tag 'Test_weights_by_strip'
    c.execute("SELECT max(wei_conf_id) from FE_CONFIG_{}_INFO where Tag='{}'".format(weight_table, tag))
    for row in c:
        wei_conf_id = row[0]
    print "New weight conf_id: ", wei_conf_id

    # Inserting weight group
    for groupid, Ws in enumerate(weights_values):
        #### NB. Weights order is inverted! From right to left.
        insert_query = u"INSERT into FE_{}_PER_GROUP_DAT (wei_conf_id, group_id, W4,W3,W2,W1,W0) \
                VALUES ({0}, {1}, {2},{3},{4},{5},{6}) ".format(weight_table, wei_conf_id, groupid, Ws[0], Ws[1],Ws[2],Ws[3],Ws[4])
        print "QUERY: ", insert_query
        if not args.dry: c.execute(insert_query)

   
    # Inserting the logic_id weight _dat
    for lid, groupid in weights_logicid.items():
        insert_query = u"INSERT into FE_CONFIG_{}_DAT (wei_conf_id, logic_id, group_id) \
                VALUES ({0},{1},{2})".format(weight_table, wei_conf_id, lid, groupid)
        print"QUERY: ", insert_query
        if not args.dry: c.execute(insert_query)


    conn.commit()

    print "\nModification on the DB done."

if __name__ == "__main__":
  main(sys.argv)

