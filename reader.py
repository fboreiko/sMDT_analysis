import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import mdtfunctions
import new_mdtCalib_functions



df = pd.read_csv('dataConverted/1_Segment_run437124_region0051_BMG2A12.csv')
chamber = 'BMG2A12'
run = '437124'

print('initial shape: ', df.shape[0])

chi2Cut = 5
df = df[~(df.seg_chi2 > chi2Cut)]

print('all chamber segments : ', df.shape[0])
# apply driftTime cut and nSegHits cut
if chamber[:3] in ['BMG', 'BME']:
    df['cut_t'] = df['mdt_t'].apply(lambda x : all(-5 < float(ss) < 195 for ss in x[1:-1].split(', ')))
    df = df[df['cut_t']]
    df = df[df['seg_nMdtHits'] > 6]
else:
    df['cut_t'] = df['mdt_t'].apply(lambda x : all(-5 < float(ss) < 750 for ss in x[1:-1].split(', ')))
    df = df[df['cut_t']]
    df = df[df['seg_nMdtHits'] > 5]
print('all segments after cut : ', df.shape[0])

# load resolution functions
##df_RtResFit = 'UM6608_RtResFit.csv'
##splitDriftTime,zs,zl,resolution_constants = new_mdtCalib_functions.getRtRes(df_RtResFit,chamber)

new_mdtCalib_functions.drawResolution(df, run, chamber)