import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import new_mdtCalib_functions
import xMdtSegment as xSeg


def drawHitPlots(df, run, chamber):
    fig, axes = plt.subplots(figsize=(15, 8), nrows=2, ncols=3)
    fig.subplots_adjust(top=0.93, bottom=0.05, left=0.02, right=0.98, wspace=0.2, hspace=0.2)
    # fig.suptitle('run%s_%s_HitPlots'%(run,chamber), fontsize=20)

    mdt_r = df.mdt_r
    f_r = new_mdtCalib_functions.conv(mdt_r)

    # mdt_adc = df_segHit.mdt_adc.astype(float)
    # mdt_r = df_segHit.mdt_r
    mdt_t = df.mdt_t
    f_t = new_mdtCalib_functions.conv(mdt_t)

    # mdt_rTrk = df_segHit.mdt_rTrk.values.astype(float)

    # driftTime spectrum
    t0_fit, tmax_fit, axes[0, 0] = new_mdtCalib_functions.fitT0Tmax(f_t, chamber, axes[0, 0])

    # driftRadius distribution
    axes[0, 1].hist(f_r, bins=150, range=[-8, 8], label='r')
    axes[0, 1].set_xlabel('driftRadius [mm]', fontsize=15)

    # driftTime vs driftRadius

    if (chamber[:3] in ['BME', 'BMG']):
        maxRadius, maxDriftTime = 7.5, 200.0
    else:
        maxRadius, maxDriftTime = 15.0, 800.0

    axes[0, 2].scatter(f_t, f_r, marker='*', s = 2, label='driftTime vs radius')
    axes[0, 2].set_ylim(0, maxRadius)
    axes[0, 2].set_xlabel('driftTime [ns]', fontsize=15)
    axes[0, 2].set_ylabel('driftRadius [mm]', fontsize=15)
    axes[0, 2].set_xlim(0, maxDriftTime)
    axes[0, 2].legend()
    axes[0, 2].grid()

    # ADC count
    mdt_adc = df.mdt_adc
    f_adc = new_mdtCalib_functions.conv(mdt_adc)

    xadc, xbins, patch = axes[1, 0].hist(f_adc, bins=75, range=[50, 350], label='adc')
    mean = np.average(f_adc)
    std = np.sqrt(np.average((f_adc - mean) ** 2))
    axes[1, 0].set_xlim(50, 350)
    axes[1, 0].set_xlabel('adcCount', fontsize=15)
    axes[1, 0].text(270, np.max(xadc) * 0.82,
                    'Entries : %d\nMean : %.3f ns\nStd Dev : %.3f' % (np.sum(xadc), mean, std), backgroundcolor='linen',
                    fontsize=10)
    axes[1, 0].grid()

    # segment chi2
    mdt_chi2 = df.seg_chi2.values.astype(float)
    axes[1, 1].hist(mdt_chi2, bins=30, range=[0, 60], label='segment chi2')
    axes[1, 1].legend()
    axes[1, 1].set_xlabel('%s segment chi2' % (chamber))

    # segment nHits
    mdt_nHits = df.seg_nMdtHits.values.astype(int)
    axes[1, 2].hist(mdt_nHits, bins=np.max(mdt_nHits), range=[0, np.max(mdt_nHits)], label='segment nHits')
    axes[1, 2].set_xlabel('%s hits per segment' % (chamber))

    plt.show()
    fig.savefig("new_%s_chamber_1Segment" % (chamber))

datafile = "dataConverted/1_Segment_run437124_region0051_BMG4A12.csv"
df = pd.read_csv(datafile)
run = 437124
chamber = datafile[-11:-4]

drawHitPlots(df, run, chamber)