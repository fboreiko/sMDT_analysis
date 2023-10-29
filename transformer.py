import uproot3 as uproot
import csv
import pandas as pd
import sys,os, time
import re
import numpy as np
import matplotlib.pyplot as plt
import muonfixedid, chamberlist
import splitter_regions_Run2


data = ['rootdata/skimmed_ntuple_run437124_lb0000_0005_region0051.csv',
        'rootdata/skimmed_ntuple_run437124_lb0003_0014_region0051.csv',
        'rootdata/skimmed_ntuple_run437124_lb0013_0018_region0051.csv',
        'rootdata/skimmed_ntuple_run437124_lb0019_0025_region0051.csv',
        'rootdata/skimmed_ntuple_run437124_lb0023_0035_region0051.csv',
        'rootdata/skimmed_ntuple_run437124_lb0026_0032_region0051.csv',
        'rootdata/skimmed_ntuple_run437124_lb0033_0044_region0051.csv',
        'rootdata/skimmed_ntuple_run437124_lb0037_0047_region0051.csv',
        'rootdata/skimmed_ntuple_run437124_lb0048_0052_region0051.csv',
        'rootdata/skimmed_ntuple_run437124_lb0053_0057_region0051.csv',
        'rootdata/skimmed_ntuple_run437124_lb0058_0062_region0051.csv',
        'rootdata/skimmed_ntuple_run437124_lb0063_0067_region0051.csv',
        'rootdata/skimmed_ntuple_run437124_lb0068_0072_region0051.csv']

t1 = open('dataConverted/run437124_region0051_BME4A13.csv', 'w', newline="")
t2 = open('dataConverted/run437124_region0051_BMG2A12.csv', 'w', newline="")
t3 = open('dataConverted/run437124_region0051_BMG4A12.csv', 'w', newline="")
t4 = open('dataConverted/run437124_region0051_BMG6A12.csv', 'w', newline="")

out1 = csv.writer(t1)
out2 = csv.writer(t2)
out3 = csv.writer(t3)
out4 = csv.writer(t4)

dfmain = pd.read_csv(data[0])
out1.writerow(dfmain.columns)
out2.writerow(dfmain.columns)
out3.writerow(dfmain.columns)
out4.writerow(dfmain.columns)

i = 0

while i < len(data):
        print('file number: ', i)
        df = pd.read_csv(data[i])
        chamberlist = df.chamber
        j = 0
        while j < len(df):
                if chamberlist[j][2:9] == 'BME4A13':
                        out1.writerow(df.values[j])
                elif chamberlist[j][2:9] == 'BMG2A12':
                        out2.writerow(df.values[j])
                elif chamberlist[j][2:9] == 'BMG4A12':
                        out3.writerow(df.values[j])
                else:
                        out4.writerow(df.values[j])
                print(j)
                j += 1
        i += 1