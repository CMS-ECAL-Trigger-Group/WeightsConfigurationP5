import pandas as pd

EB = pd.read_csv("ChannelNumberingEB.csv", sep=',')
EE = pd.read_csv("ChannelNumberingEE.csv", sep=',')

EBparams = EB[EB["Xtal in VFE"]==1][["stripid","CMSSWID", "FED", "TT", "VFE"]]
EEparams = EE[EE["Xtal in VFE"==1]][["stripid", "CMSSWID", "FED", "CCU", "VFE"]]


EBparams.to_csv("params_EB.csv", index=False, sep=",")
EEparams.to_csv("params_EE.csv", index=False, sep=",")

