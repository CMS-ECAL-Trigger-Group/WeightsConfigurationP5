# Weights groups preparation

## Strip parameters

The files `ChannelNumberingEB.csv` and `ChannelNumberingEE.csv` contain a full mapping of all the strips in EB and EE of
ECAL. For weights gymnastic we would need only the following information: 

- `stripid` used to identify the strip in the Weights studies and in the input files for ECALTPGParamBuilder
- `cmsswid` general identifier used in CMSSW and CondDB (offline DB)
- `logidid` used to identify the strip in the ConfDB, the online P5 DB for configuration

The `stripid`, `cmsswid` and the mapping needed to idenitify the logicid are extracted from the full maps in
`ChannelNumbering*.csv` and saved for convenience in `params_EB.txt` and `params_EE.txt`. 

Then, the confDB is directly queried to the fetch the `logicids` in the DB. To perform this task the scripts
`logicid_retriver_E*.py` are used. The output is `params_E*_logicid.txt` files. 
EE and EB are split because the mapping in the confDB is different between them. Please checkout the `logicid_retriver`
scripts to have a look at which column of the `channelview` table of the ConfDB is used to retrive the logicid. This
is the same mapping used by the [ECALTPGParamBuilder](https://github.com/cms-sw/cmssw/blob/master/CalibCalorimetry/EcalTPGTools/plugins/EcalTPGParamBuilder.cc#L846).
    

```bash
python logicid_retriver_EB.py  ***password***
python logicid_retriver_EE.py  ***password***
```

## Weight configuration

The ECAL TPG weight configuration is based on WeightGroups and WeightIDMap: 

- WeightGroups:  set of 5 encoded numbers representing the weights
- WeightIDMap: map between each stripid/logicid to a weight group. 

This structure is kept in the confDB and condDB. Two files representing this structure are needed for the
ECALTPGParamBuilder to build the DB tags. 

