# Run the script in a computer with oracle libraries
# x2go machines should be fine
import sys
import cx_Oracle
import random

conn_str = u'CMS_ECAL_CONF/0r4cms_3c4lc0nf@cms_tstore'

def main(argv):

  conn = cx_Oracle.connect(conn_str)
  c = conn.cursor()

  logic_ids = []

  c.execute(u"SELECT logic_id from FE_CONFIG_WEIGHT_DAT where wei_conf_id={}".format(argv[1]))
  for row in c:
    logic_ids.append(row[0])


  # Get last version with tag 'Test_weights_by_strip'
  c.execute("SELECT max(wei_conf_id) from FE_CONFIG_WEIGHT_INFO where Tag='Test_weights_by_strip'")
  for row in c:
    wei_conf_id = row[0]
  print "Weight conf_id: ", wei_conf_id

  # insert_info_query = u"INSERT into FE_CONFIG_WEIGHT_INFO (wei_conf_id, tag, version, number_of_groups, db_timestamp) \
  #           VALUES (FE_CONFIG_WEIGHT_SQ.nextval, 'Test_weights_by_strip', 1, 1000, CURRENT_TIMESTAMP) "
  # c.execute(insert_info_query)
  # conn.commit()

  # for ig in range(1000):
  #   insert_info_query = u"INSERT into FE_WEIGHT_PER_GROUP_DAT (wei_conf_id, group_id, W0,W1,W2,W3,W4) \
  #            VALUES ({0}, {1}, {2},{3},{4},{5},{6}) ".format(wei_conf_id, ig, random.randrange(257),random.randrange(257),
  #             random.randrange(257),random.randrange(257),random.randrange(257))
  #   print(insert_info_query)
  #   c.execute(insert_info_query)
  
  # conn.commit()

  for lid in logic_ids:
    insert_query = u"INSERT into FE_CONFIG_WEIGHT_DAT (wei_conf_id, logic_id, group_id) \
          VALUES ({0},{1},{2})".format(wei_conf_id, lid, random.randrange(1000))
    print(insert_query)
    c.execute(insert_query)
  
  conn.commit()

#       print "\nModification on the DB done."

if __name__ == "__main__":
  main(sys.argv)

