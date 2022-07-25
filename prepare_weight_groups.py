import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--wEE", type=str, help="Weights file EE", required=True)
parser.add_argument("--wEB", type=str, help="Weights file EB", required=True)
parser.add_argument("--PU", type=int, help="PU weights" , required=True)
parser.add_argument("--S", type=str, help="S weights", required=True )
parser.add_argument("-o", "--output", type=str, help="Output name", required=True)
args = parser.parse_args()


weightsEE = pd.read_csv(args.wEE,  sep=',', float_precision='round_trip')
weightsEB = pd.read_csv(args.wEB,  sep=',', float_precision='round_trip')

# The original contains the ID map of the strip and 1 or 0 for EE or EB
group_orig = pd.read_csv("EcalTPGWeightGroup_original.txt", sep=" ", header=None)



stripids_map = {}
# Defaults weights groups for EB and EE
wgroups = [[92,93,16,159,24], [86,95,16,161,26]]
Sbin = args.S
PU = args.PU

def add_8th_bit(num):
    return  int(num) | 0x80

for _, row in weightsEE[(weightsEE.PU==PU) & (weightsEE.Sbin ==Sbin)].iterrows():
    group = list(map(int,[row.enc_w_1_1, row.enc_w_1_2, row.enc_w_1_3, add_8th_bit(row.enc_w_1_4), row.enc_w_1_5]))
    try:
        index = wgroups.index(group)
        stripids_map[row.stripid] = index
    except ValueError:
        stripids_map[row.stripid] = len(wgroups)
        wgroups.append(group)
  
        


for _, row in weightsEB[(weightsEB.PU==PU) & (weightsEB.Sbin ==Sbin)].iterrows():
    group = list(map(int,[row.enc_w_1_1, row.enc_w_1_2, row.enc_w_1_3, add_8th_bit(row.enc_w_1_4), row.enc_w_1_5]))
    try:
        index = wgroups.index(group)
        stripids_map[row.stripid] = index
    except ValueError:
        stripids_map[row.stripid] = len(wgroups)
        wgroups.append(group)
  
        
 


for j in group_orig.index:
    strip = group_orig.loc[j,0] 
    det = group_orig.loc[j,1]   

    if strip in stripids_map:
        group_orig.loc[j,1] = stripids_map[strip]
    
    # If not present leave the default two groups

idmap = pd.DataFrame(wgroups)
group_orig.to_csv("EcalTPGWeightGroup_{}.txt".format(args.output), sep=' ', index=False, header=None)
idmap.to_csv("EcalTPGWeightIdMap_{}.txt".format(args.output), sep=' ', index=False, header=None)