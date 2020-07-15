import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dof", type=str, help="DOF file")
parser.add_argument("--wEE", type=str, help="Weights file EE")
parser.add_argument("--wEB", type=str, help="Weights file EB")
parser.add_argument("--PU", type=int, help="PU weights" )
parser.add_argument("--S", type=str, help="S weights" )
parser.add_argument("-o", "--output", type=str, help="Output name")
args = parser.parse_args()


dof = pd.read_csv(args.dof,  sep=',', float_precision='round_trip')
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
    group = list(map(int,[row.encw1, row.encw2, row.encw3, add_8th_bit(row.encw4), row.encw5]))
    index = wgroups.index(group)
    if index == -1: 
        stripids[row.stripid] = len(wgroups)
        wgroups.append(group)
    else:
        stripids[row.stripid] = index


for _, row in weightsEB[(weightsEB.PU==PU) & (weightsEB.Sbin ==Sbin)].iterrows():
    group = list(map(int,[row.encw1, row.encw2, row.encw3, add_8th_bit(row.encw4), row.encw5]))
    index = wgroups.index(group)
    if index == -1: 
        stripids[row.stripid] = len(wgroups)
        wgroups.append(group)
    else:
        stripids[row.stripid] = index  


for j in group_orig.index:
    strip = group_orig.loc[j,0] 
    det = group_orig.loc[j,1]   

    if strip in stripids:
        group_orig.loc[j,1] = stripids[strip]
    
    # If not present leave the default two groups

idmap = pd.DataFrame(wgroups)
group_orig.to_csv("EcalTPGWeightGroup_{}.txt".format(args.output), sep=' ', index=False, header=None)
idmap.to_csv("EcalTPGIdMap_{}.txt".format(args.output), sep=' ', index=False, header=None)