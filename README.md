# Weights groups preparation

## Strip parameters

The files `ChannelNumberingEB.csv` and `ChannelNumberingEE.csv` contain a full mapping of all the strips in EB and EE of
ECAL. For weights gymnastic we would need only the following information: 

- `stripid` used to identify the strip in the Weights studies and in the input files for ECALTPGParamBuilder
- `cmsswid` general identifier used in CMSSW and CondDB (offline DB)
- `logidid` used to identify the strip in the ConfDB, the online P5 DB for configuration

The `stripid`, `cmsswid` and the mapping needed to idenitify the logicid are extracted from the full maps in
`ChannelNumbering*.csv` and saved for convenience in `params_EB.csv` and `params_EE.csv`. 

To extract these files execute the script:
```bash
python get_params_EEEB.py
```

Then, the confDB is directly queried to the fetch the `logicids` in the DB. To perform this task the script
`logicid_retriver.py` are used. The output is `params_E*_logicid.txt` files. 
EE and EB are split because the mapping in the confDB is different between them. Please checkout the `logicid_retriver`
scripts to have a look at which column of the `channelview` table of the ConfDB is used to retrive the logicid. 

- EB: logicid of the strip by mapping: FED, TT, VFE
- EE: logicid of the strip by mapping: FED, CCU, VFE

This is the same mapping used by the [ECALTPGParamBuilder](https://github.com/cms-sw/cmssw/blob/master/CalibCalorimetry/EcalTPGTools/plugins/EcalTPGParamBuilder.cc#L846).
    

```bash
python logicid_retriver.py  -h
usage: logicid_retriver.py [-h] -i INPUTFILE -o OUTPUTFILE -s SUBDET -p
                           PASSWORD

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputfile INPUTFILE
                        Input parameters file
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        Output file
  -s SUBDET, --subdet SUBDET
                        Subdetector EB/EE
  -p PASSWORD, --password PASSWORD
                        ConfDB password
                        
python logicid_retriver.py  -i params_EB.csv -o params_EB_logicid.csv -s EB -p ****
python logicid_retriver.py  -i params_EE.csv -o params_EE_logicid.csv -s EE -p ****

```
Finally all the logicids have been concatenated in a single file **params_EBEE_logicids.csv**.

For a general introduction to the ECAL trigger primitive generation have a look at [Davide's thesis](https://dvalsecc.web.cern.ch/dvalsecc/PhD_Thesis/thesis_Valsecchi_final.pdf).

## Weight configuration

The ECAL TPG weight configuration is based on WeightGroups and WeightIDMap: 

- WeightGroups:  set of 5 encoded numbers representing the weights.
- WeightIDMap: map between each stripid/logicid to a weight group. 

This structure is kept in the confDB and condDB. Two files representing this structure are needed for the
ECALTPGParamBuilder to build the DB tags. 

In the configuration created by this repo and for the ECALTPGParamBuilder inputs the weights must be encoded, but
specified in the natural ordering (w0,w1,w2,w3,w4). Moreover, the 8th bit of weight, which signal to the electronics the
position of the peak must NOT be included, since it is automatically added by the configuration code. 

### Weights encoding:

The weights are encoded following the formula:

    W_encoded (1 - sign(W))*64 + W*64

Then a nearest integer approximation is performed. Since the sum of the 5 weights must be always 0, there is a special code to
perform the approximation in the best way:
[script](https://gitlab.cern.ch/cms-ecal-dpg/ecall1algooptimization/-/blob/master/PileupMC/weights_encoder.py)

### Weight configuration creator

### Weight manual upload

A script has been prepared to manually load a set of weights in the ConfDB for manual tests on the system. 

**N.B.: This is not the standard way to interact with the Weights configuration!! Very dangerous!! Every weights
configuration should pass through the ECALTPGParamBuilder**. 

```bash
 python load_weights.py -h
usage: load_weights.py [-h] [-d] -t TAG --wg WG --wi WI [-l LOGICIDS] -p
                       PASSWORD

optional arguments:
  -h, --help            show this help message and exit
  -d, --dry             Dry run
  -t TAG, --tag TAG     Tag
  --wg WG               Weight group file
  --wi WI               Weight ID map
  -l LOGICID, --logicid LOGICID
                        Logicid mapping
  -p PASSWORD, --password PASSWORD
                        ConfDB password

```

The script needs WeightGroup and WeightIDMap files and the confDb password. It creates an entry in the necessary tables
with the specified `tag`. 

The code should be run into the `x2go` machine in the CMS network, with `python2` where the Oracle DB python libraries
are installed in the system. 

For example: 

```bash
python load_weights.py -t TEST --dry --wg output_files/EcalTPGWeightGroup_2018_PU50_S2.txt 
    --wi output_files/EcalTPGWeightIdMap_2018_PU50_S2.txt --password ******

N weights 627
New weight conf_id:  None
QUERY:  INSERT into FE_WEIGHT_PER_GROUP_DAT (wei_conf_id, group_id, W4,W3,W2,W1,W0)                 VALUES (None, 0, 92,93,16,159,24) 
QUERY:  INSERT into FE_WEIGHT_PER_GROUP_DAT (wei_conf_id, group_id, W4,W3,W2,W1,W0)                 VALUES (None, 7, 85,94,18,162,25) 
QUERY:  INSERT into FE_WEIGHT_PER_GROUP_DAT (wei_conf_id, group_id, W4,W3,W2,W1,W0)                 VALUES (None, 8, 83,96,19,161,25) 
QUERY:  INSERT into FE_WEIGHT_PER_GROUP_DAT (wei_conf_id, group_id, W4,W3,W2,W1,W0)                 VALUES (None, 12, 84,95,18,162,25) 
QUERY:  INSERT into FE_WEIGHT_PER_GROUP_DAT (wei_conf_id, group_id, W4,W3,W2,W1,W0)                 VALUES (None, 13, 84,95,19,161,25) 
QUERY:  INSERT into FE_WEIGHT_PER_GROUP_DAT (wei_conf_id, group_id, W4,W3,W2,W1,W0)                 VALUES (None, 14, 85,95,17,161,26) 
[.................]
QUERY:  INSERT into FE_CONFIG_WEIGHT_DAT (wei_conf_id, logic_id, group_id)                 VALUES (None,1216021205,287)
QUERY:  INSERT into FE_CONFIG_WEIGHT_DAT (wei_conf_id, logic_id, group_id)                 VALUES (None,1216021201,74)
QUERY:  INSERT into FE_CONFIG_WEIGHT_DAT (wei_conf_id, logic_id, group_id)                 VALUES (None,1216021203,83)
QUERY:  INSERT into FE_CONFIG_WEIGHT_DAT (wei_conf_id, logic_id, group_id)                 VALUES (None,1216021202,75)
QUERY:  INSERT into FE_CONFIG_WEIGHT_DAT (wei_conf_id, logic_id, group_id)                 VALUES (None,1151052401,574)
QUERY:  INSERT into FE_CONFIG_WEIGHT_DAT (wei_conf_id, logic_id, group_id)                 VALUES (None,1151052403,580)
QUERY:  INSERT into FE_CONFIG_WEIGHT_DAT (wei_conf_id, logic_id, group_id)                 VALUES (None,1151052402,583)
QUERY:  INSERT into FE_CONFIG_WEIGHT_DAT (wei_conf_id, logic_id, group_id)                 VALUES (None,1151052405,584)
QUERY:  INSERT into FE_CONFIG_WEIGHT_DAT (wei_conf_id, logic_id, group_id)                 VALUES (None,1151052404,575)
[.............]
```


### Random weights creator

The script `random_weights_uploader.py` creates a special configuration in which each script gets a random set of
weights. 
Since the weights are not normalized to 0 this configuration creates large energy TPs in the detectors. 

```bash
python random_weights_uploader.py
```
