import os 
import sys
import cx_Oracle

conn_str = u'CMS_ECAL_CONF/0r4cms_3c4lc0nf@cms_tstore'

strips = []
with open("params_EB.txt") as file:
    for l in file.readlines():
        strips.append(list(map(int, l.split(","))) )



def main(argv):

    conn = cx_Oracle.connect(conn_str)
    c = conn.cursor()

    query = "SELECT ID1,ID2,ID3,logic_id from channelview where  NAME='ECAL_readout_strip' and MAPS_TO='EB_VFE'"
    c.execute(query)

    logid = {}
    for row in c:
        logid[(row[0], row[1], row[2])] = row[3]

    
    for strip in strips :
        strip.append(logid[(strip[2], strip[3], strip[4])])

    with open("params_EB_logicid.txt", "w") as of:
        for strip in strips:
            of.write(",".join(map(str,strip)) +"\n")


if __name__ == "__main__":
    main(sys.argv)