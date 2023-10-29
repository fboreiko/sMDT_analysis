import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def conv(df):
    return np.hstack(np.array([[float(st) for st in item.strip('[]\s').split(',')] for item in list(df.values)]))

chamber = 'BMG2A12'
run = '437124'
df = pd.read_csv('/Users/fedorboreiko/PycharmProjects/roottocsv/dataConverted/run437124_region0051_BMG2A12.csv')

unbias = df.unbias_rTrk_new
new = df.rTrk_new
r = df.mdt_r
resi = df.mdt_resi

f_unbias = conv(unbias)
f_r = conv(r)
f_new = conv(new)
f_resi = conv(resi)

resi_new = np.abs(f_r) - np.abs(f_new)
resi_unbias = np.abs(f_r) - np.abs(f_unbias)

fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(top=0.93, bottom=0.10, left=0.10, right=0.98, wspace=0.2, hspace=0.2)

ax.hist2d(f_r, f_resi*1000, bins=(150, 450), cmap=plt.cm.jet)
ax.set_ylim([-500, 500])

plt.suptitle('%s Track Hit Residuals vs Radius' % chamber, fontsize=20)
plt.savefig("/Users/fedorboreiko/PycharmProjects/roottocsv/Else/%s_TrackResiduals_vs_Radius" % chamber)
plt.show()