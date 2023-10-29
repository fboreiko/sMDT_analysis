import pandas as pd
import sys,os, time,math
import re, glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import muonfixedid, chamberlist
import splitter_regions_Run2
import mdtCalib_functions


# pre-defined functions
# function to convert single columns string data to np.array
def conv(df):
    return np.hstack(np.array([[float(st) for st in item.strip('[]\s').split(',')] for item in list(df.values)]))


# function to convert RT paraments
def convertRtConstants(da):
    zs = np.array([float(x) for x in da.values[0][5][1:-1].split(', ')])
    zl = np.array([float(x) for x in da.values[0][8][1:-1].split(', ')])
    z = np.array([float(x) for x in da.values[0][11][1:-1].split(', ')])
    splitDriftTime = float(da.values[0][3])
    diffJointPoint = float(da.values[0][4])
    return zs, zl, z, splitDriftTime, diffJointPoint


# function to check efficiency
def check_3sigma(df_eff):
    if df_eff.resi_unbias > 3 * df_eff.res_Sigma:
        return False
    else:
        return True


def check_5sigma(df_eff):
    if df_eff.resi_unbias > 5 * df_eff.res_Sigma:
        return False
    else:
        return True


def check_hardware(df_eff):
    if df_eff.rTrk_unbias > maxRadius:
        return False
    else:
        return True


# data = 'run358395_refitOff_region0178_EIL2C11_refittedSegment_refitOff.csv'
chamber = 'BME4A13'
run = '437124'
df = pd.read_csv('/Users/fedorboreiko/PycharmProjects/roottocsv/dataConverted/1_Segment_run437124_region0051_BME4A13.csv')

# apply segment on track and chi2 cut
# df = df[df.onTrkFlag == True]
minChi2 = 1000
df = df[df.seg_chi2 < minChi2]
print(run, chamber, df.shape[0])

# apply driftTime cut and nSegHits cut
if chamber[:3] in ['BMG', 'BME']:
    df['cut_t'] = df['mdt_t'].apply(lambda x: all(0 < float(ss) < 186 for ss in x[1:-1].split(', ')))
    df = df[df['cut_t']]
    df = df[df['seg_nMdtHits'] > 6]
else:
    df['cut_t'] = df['mdt_t'].apply(lambda x: all(0 < float(ss) < 750 for ss in x[1:-1].split(', ')))
    df = df[df['cut_t']]
    df = df[df['seg_nMdtHits'] > 5]
print('all segments after cut : ', df.shape[0])

# load data columns
unbias = df.unbias_rTrk_new
new = df.rTrk_new
r = df.mdt_r
resi = df.mdt_resi
f_unbias = conv(unbias)
f_new = conv(new)
f_r = conv(r)
f_resi = conv(resi)
resi = np.abs(f_r) - np.abs(f_new)
resi_new = np.abs(f_r) - np.abs(f_new)
resi_unbias = np.abs(f_r) - np.abs(f_unbias)

maxRadius, maxDriftTime, step, npad = 14.6, 800.0, 1, 16
# splitBin = 13  # sMDT = 25  MDT = 13
if (chamber[:3] in ['BME', 'BMG']):
    maxRadius, maxDriftTime, step, npad = 7.1, 200.0, 1, 8

# load resolution functions and calculate resolution for each hits
df_RtResFit = '/Users/fedorboreiko/PycharmProjects/roottocsv/UM6608_RtResFit.csv'
splitDriftTime, zs, zl, resolution_constants = mdtCalib_functions.getRtRes(df_RtResFit, chamber)
print(chamber, splitDriftTime, zs, zl, resolution_constants)
resSigma = np.polyval(resolution_constants, np.abs(f_new)) / 1000.
print(resSigma)

# create a new dataframe for calcuating efficiency
df_eff = pd.DataFrame({'radius': f_r, 'rTrk_new': f_new, 'rTrk_unbias': f_unbias, 'res_Sigma': resSigma,
                       'resi_unbias': np.abs(resi_unbias)})

#df_eff['sigma3_flag'] = df_eff.apply(check_3sigma, axis=1)
df_eff['sigma5_flag'] = df_eff.apply(check_5sigma, axis=1)
df_eff['sigmaHardware_flag'] = df_eff.apply(check_hardware, axis=1)

df_eff.head()

# set radius interval
startSlice = np.arange(0.1, maxRadius, step)
stopSlice = np.append(startSlice[1:], maxRadius)
branchBasket = list(zip(*(startSlice, stopSlice)))

#n3_eff = []
n5_eff = []
h_eff = []
for n in range(len(branchBasket)):
    radius_filter = (df_eff.rTrk_new < branchBasket[n][1]) & (df_eff.rTrk_new > branchBasket[n][0])
    #count3 = df_eff.sigma3_flag[radius_filter]
    # print(n,len(count3),np.sum(count3))
    #n3_eff.append(100.0 * np.sum(count3) / len(count3))
    count5 = df_eff.sigma5_flag[radius_filter]
    n5_eff.append(100.0 * np.sum(count5) / len(count5))
    count_h = df_eff.sigmaHardware_flag[radius_filter]
    # print(n,len(count),np.sum(count))
    h_eff.append(100.0 * np.sum(count_h) / len(count_h))

print(n5_eff, h_eff)

# plot eff sigma3, sigma5, hardware
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(top=0.93, bottom=0.10, left=0.10, right=0.98, wspace=0.2, hspace=0.2)

ax.plot(np.arange(7), h_eff, 'bo', label='Hardware Efficiency')
ax.plot(np.arange(7), n5_eff, 'rs', label='5 Sigma Efficiency')
#ax.plot(np.arange(7), n3_eff, '^', color = 'grey', label='3 Sigma Efficiency')

ax.set_ylabel('Efficiency %', fontsize=15)
ax.set_xlabel('Raidus [mm]', fontsize=15)
ax.set_ylim(50, 105)
ax.set_yticks(np.arange(50, 101, step=5))

ax.grid()
ax.legend(fontsize=20)
plt.suptitle('Run%s_%s_Efficiency_chi2cut%s' % (run, chamber, minChi2), fontsize=20)

plt.savefig("/Users/fedorboreiko/PycharmProjects/roottocsv/Efficiency_Run%s_%s_chi2cut%d_1Segment.png" % (run, chamber, minChi2))

plt.show()