import uproot
import pandas as pd
import sys,os, time
import re
import numpy as np
import matplotlib.pyplot as plt

import mdtfunctions
import muonfixedid, chamberlist
import splitter_regions_Run2
import mdtCalib_functions

file = 'dataConverted/run437124_region0104_BMG2C14.csv'
df = pd.read_csv(file)
chamber = file[-11:-4]

df_RtResFit = 'UM6608_RtResFit.csv'
splitDriftTime, zs, zl, resolution_constants = mdtCalib_functions.getRtRes(df_RtResFit, chamber)

df1 = pd.DataFrame(columns = ['rTrk_new', 'unbias_rTrk_new'], index = np.arange(0, len(df), 1))
print(df1)

q = 0

'''flag, rTrk_new, track_chi2_new, track_chi2_default, refit_m, refit_b, unbias_rTrk_new = mdtfunctions.refitSegment(422, df, resolution_constants)
# df1 = df1.append({'rTrk_new' : rTrk_new, 'unbias_rTrk_new' : unbias_rTrk_new}, ignore_index=True)
print('Initially on {}: {}'.format(422, df.mdt_rTrk[q]))
print('rTrk_new on {}: {}'.format(422, rTrk_new))
print('unbias_rTrk_new on {}: {}'.format(422, unbias_rTrk_new))'''


#df1 = df1.append({'rTrk_new' : rTrk_new, 'unbias_rTrk_new' : unbias_rTrk_new}, ignore_index=True)
while q < len(df):
        flag, rTrk_new, track_chi2_new, track_chi2_default, refit_m, refit_b, unbias_rTrk_new = mdtfunctions.refitSegment(q, df, resolution_constants)
        df1.loc[q] = [rTrk_new, unbias_rTrk_new]
        #print('On {} : {}'.format(q, rTrk_new))
        #print('On {} : {}'.format(q, unbias_rTrk_new))
        q += 1
print('len before: ', len(df1.unbias_rTrk_new))
print('len of f1: ', len(df1))
a = len(df1)
i = 0
sum = 0
while i < a:
    if str(df1.unbias_rTrk_new[i])[1:6] == "-99.0":
        df1 = df1.drop(labels=i, axis=0)
        print('here on: ', i)
        i += 1
        sum += 1
    else:
        i += 1
print('sum: ', sum)
print('len after: ', len(df1.values))
print('end of looping')

'''print(df1.values[0][0])
print(type(df1.values[0][0]))
print(df1.values[0][0][0])'''
#out = df1.groupby(level=0).agg(list)
outfinal = pd.concat([df1, df.reindex(df1.index)], axis=1)
#outfinal = pd.concat([df1, df], axis=1, join="inner")
outfinal.to_csv('dataConverted/run437124_region0104_BMG2C14.csv')