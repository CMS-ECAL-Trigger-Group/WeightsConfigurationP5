import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l","--logicid", help="Logicid mapping", default="params_EBEE_logicid.csv")
parser.add_argument("-i","--inputfile", type=str, help="Input file", required=True)
parser.add_argument("-o","--outputfile", type=str, help="Output file", required=True)
args = parser.parse_args()


gmap = pd.read_csv(args.logicid, sep=",")

final_map = []
for lid in gmap.stripid:
    final_map[lid] = 0


with open(args.inputfile) as lm: 
    for l in lm.readlines():
        if l.startswith("#"): continue
        n = l.strip().split(" ")
        if n[0] == "ALL":
            # set all the strips to the value
            for k in final_map.keys():
                final_map[k] = n[1]
        if n[0] == "FED":
            # set all the strips with the FED to value
            for strip in gmap[gmap.FED == n[1]].stripid:
                final_map[strip] = n[2]
        if n[0] == "STRIP":
            final_map[n[1]] = n[2]
        if n[0] == "SUBDET":
            if n[1] == "EB":
                for strip in gmap[(gmap.FED >= 610)&(gmap.FED <=645)].stripid:
                    final_map[strip] = n[2]
            if n[1] == "EE":
                for strip in gmap[(gmap.FED < 610)&(gmap.FED >645)].stripid:
                    final_map[strip] = n[2]
            if n[1] == "EE-":
                for strip in gmap[(gmap.FED < 610)].stripid:
                    final_map[strip] = n[2]
            if n[1] == "EE+":
                for strip in gmap[(gmap.FED > 610)].stripid:
                    final_map[strip] = n[2]

# Write the final IDMap file
with open(args.outputfile, "w") as of:
    for k,v in final_map.items():
        of.write("{} {}\n".format(k,v))


