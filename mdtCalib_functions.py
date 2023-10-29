#!/usr/bin/env python
# coding: utf-8
import uproot
import pandas as pd
import sys, os, time, math
import re, glob
import numpy as np
import muonfixedid, chamberlist
import splitter_regions_Run2
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# tangentLine function, input two circles data (x,y,r), output 8 points (4 tangentLine coordinators)
def tangentLine(circle1, circle2, plotting):
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    # print(circle1,circle2)
    # make sure r1 > r2
    if r1 < r2:
        x1, y1, r1 = circle2
        x2, y2, r2 = circle1
        # print(r1,r2)
    # setup output list(tuple)
    # line1 = xt1,yt1,xt3,yt3
    # line2 = xt2,yt2,xt4,yt4
    # line3 = xt5,yt5,xt7,yt7
    # line4 = xt6,yt6,xt8,yt8
    # tangent = [line1,line2,line3,line4]
    tangent = []

    # case r1 == r2 == 0
    if r1 == 0 and r2 == 0:
        line1 = x1, y1, x2, y2
        line2 = x1, y1, x2, y2
        line3 = x1, y1, x2, y2
        line4 = x1, y1, x2, y2

        tangent.append(line1)
        tangent.append(line2)
        tangent.append(line3)
        tangent.append(line4)
        return tangent
    elif r2 == 0:  # no case of r1 == 0
        xo, yo = x2, y2
        xt3, yt3, xt4, yt4 = x2, y2, x2, y2
        xt7, yt7, xt8, yt8 = x2, y2, x2, y2
        # step 1 : calc the inner tangent point xt1,yt1,xt2,yt2
        xt1 = (r1 ** 2 * (xo - x1) + r1 * (yo - y1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + x1
        yt1 = (r1 ** 2 * (yo - y1) - r1 * (xo - x1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + y1
        # s = np.round((y1-yt1)*(yo-yt1)/((xt1-x1)*(xt1-xo)))
        xt2 = (r1 ** 2 * (xo - x1) - r1 * (yo - y1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + x1
        yt2 = (r1 ** 2 * (yo - y1) + r1 * (xo - x1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + y1
        # step 2 : calc the inner tangent point xt5,yt5,xt6,yt6
        xt5 = (r1 ** 2 * (xo - x1) + r1 * (yo - y1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + x1
        yt5 = (r1 ** 2 * (yo - y1) - r1 * (xo - x1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + y1
        # s = np.round((y1-yt1)*(yo-yt1)/((xt1-x1)*(xt1-xo)))
        xt6 = (r1 ** 2 * (xo - x1) - r1 * (yo - y1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + x1
        yt6 = (r1 ** 2 * (yo - y1) + r1 * (xo - x1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + y1
        if plotting == 1:
            ax2.plot(np.array([xt1, xt3]), np.array([yt1, yt3]), 'r--', label='outerTangent1')
            ax2.plot(np.array([xt2, xt4]), np.array([yt2, yt4]), 'b--', label='outerTangent2')
            ax2.plot(np.array([xt5, xt7]), np.array([yt5, yt7]), 'g--', label='innerTangent1')
            ax2.plot(np.array([xt6, xt8]), np.array([yt6, yt8]), 'k--', label='innerTangent2')
        line1 = xt1, yt1, xt3, yt3
        line2 = xt2, yt2, xt4, yt4
        line3 = xt5, yt5, xt7, yt7
        line4 = xt6, yt6, xt8, yt8
        tangent.append(line1)
        tangent.append(line2)
        tangent.append(line3)
        tangent.append(line4)
        return tangent

    # case r1 or r2 == 0 and r1==r2
    elif r1 == r2:
        theta = 0.
        if (x2 - x1) == 0:
            theta = np.pi / 2.
        else:
            theta = np.arctan((y2 - y1) / (x2 - x1))
            # step 1 : calculate parallel outer tangent lines
        xt1 = x1 + r1 * np.sin(theta)
        xt2 = x1 - r1 * np.sin(theta)
        yt1 = y1 - r1 * np.cos(theta)
        yt2 = y1 + r1 * np.cos(theta)

        xt3 = x2 + r2 * np.sin(theta)
        xt4 = x2 - r2 * np.sin(theta)
        yt3 = y2 - r2 * np.cos(theta)
        yt4 = y2 + r2 * np.cos(theta)

        # step 2 : find the inner tangent lines intersction point (xi,yi) makesure r1 > r2
        xo = (x2 * r1 + x1 * r2) / (r1 + r2)
        yo = (y2 * r1 + y1 * r2) / (r1 + r2)
        # print(r1,r2,xo,yo)
        # ax2.plot(np.array([x1,x2,xo]),np.array([y1,y2,yo]),'b-')
        # step 5 : calc the inner tangent point xt5,yt5 ... xt8,yt8
        xt5 = (r1 ** 2 * (xo - x1) + r1 * (yo - y1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + x1
        yt5 = (r1 ** 2 * (yo - y1) - r1 * (xo - x1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + y1
        # s = np.round((y1-yt1)*(yo-yt1)/((xt1-x1)*(xt1-xo)))
        xt6 = (r1 ** 2 * (xo - x1) - r1 * (yo - y1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + x1
        yt6 = (r1 ** 2 * (yo - y1) + r1 * (xo - x1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + y1
        # print(xt5,yt5,xt6,yt6,s)
        xt7 = (r2 ** 2 * (xo - x2) + r2 * (yo - y2) * np.sqrt((xo - x2) ** 2 + (yo - y2) ** 2 - r2 ** 2)) / (
                    (xo - x2) ** 2 + (yo - y2) ** 2) + x2
        yt7 = (r2 ** 2 * (yo - y2) - r2 * (xo - x2) * np.sqrt((xo - x2) ** 2 + (yo - y2) ** 2 - r2 ** 2)) / (
                    (xo - x2) ** 2 + (yo - y2) ** 2) + y2
        # ss = np.round((y3-yt3)*(yo-yt3)/((xt3-x3)*(xt3-xo)))
        xt8 = (r2 ** 2 * (xo - x2) - r2 * (yo - y2) * np.sqrt((xo - x2) ** 2 + (yo - y2) ** 2 - r2 ** 2)) / (
                    (xo - x2) ** 2 + (yo - y2) ** 2) + x2
        yt8 = (r2 ** 2 * (yo - y2) + r2 * (xo - x2) * np.sqrt((xo - x2) ** 2 + (yo - y2) ** 2 - r2 ** 2)) / (
                    (xo - x2) ** 2 + (yo - y2) ** 2) + y2
        if plotting == 1:
            ax2.plot(np.array([xt1, xt3]), np.array([yt1, yt3]), 'r--', label='outerTangent1')
            ax2.plot(np.array([xt2, xt4]), np.array([yt2, yt4]), 'b--', label='outerTangent2')
            ax2.plot(np.array([xt5, xt7]), np.array([yt5, yt7]), 'g--', label='innerTangent1')
            ax2.plot(np.array([xt6, xt8]), np.array([yt6, yt8]), 'k--', label='innerTangent2')

        line1 = xt1, yt1, xt3, yt3
        line2 = xt2, yt2, xt4, yt4
        line3 = xt5, yt5, xt7, yt7
        line4 = xt6, yt6, xt8, yt8
        tangent.append(line1)
        tangent.append(line2)
        tangent.append(line3)
        tangent.append(line4)
        return tangent
    else:  # all the normal cases
        # step 1 : find the outer tangent lines intersction point (xo,yo) makesure r1 > r2
        xo = (x2 * r1 - x1 * r2) / (r1 - r2)
        yo = (y2 * r1 - y1 * r2) / (r1 - r2)
        # print(r1,r2,xo,yo)
        # ax2.plot(np.array([x1,x2,xo]),np.array([y1,y2,yo]),'b-')
        # step 2 : calc the tangent point xt1,yt1 ... xt4,yt4
        xt1 = (r1 ** 2 * (xo - x1) + r1 * (yo - y1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + x1
        yt1 = (r1 ** 2 * (yo - y1) - r1 * (xo - x1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + y1
        # s = np.round((y1-yt1)*(yo-yt1)/((xt1-x1)*(xt1-xo)))
        xt2 = (r1 ** 2 * (xo - x1) - r1 * (yo - y1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + x1
        yt2 = (r1 ** 2 * (yo - y1) + r1 * (xo - x1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + y1
        # print(xt1,yt1,xt2,yt2,s)
        # if s != 1 :
        #    tmp = yt1
        #    yt1 = yt2
        #    yt2 = tmp
        xt3 = (r2 ** 2 * (xo - x2) + r2 * (yo - y2) * np.sqrt((xo - x2) ** 2 + (yo - y2) ** 2 - r2 ** 2)) / (
                    (xo - x2) ** 2 + (yo - y2) ** 2) + x2
        yt3 = (r2 ** 2 * (yo - y2) - r2 * (xo - x2) * np.sqrt((xo - x2) ** 2 + (yo - y2) ** 2 - r2 ** 2)) / (
                    (xo - x2) ** 2 + (yo - y2) ** 2) + y2
        # ss = np.round((y3-yt3)*(yo-yt3)/((xt3-x3)*(xt3-xo)))
        xt4 = (r2 ** 2 * (xo - x2) - r2 * (yo - y2) * np.sqrt((xo - x2) ** 2 + (yo - y2) ** 2 - r2 ** 2)) / (
                    (xo - x2) ** 2 + (yo - y2) ** 2) + x2
        yt4 = (r2 ** 2 * (yo - y2) + r2 * (xo - x2) * np.sqrt((xo - x2) ** 2 + (yo - y2) ** 2 - r2 ** 2)) / (
                    (xo - x2) ** 2 + (yo - y2) ** 2) + y2
        # print(xt3,yt3,xt4,yt4,ss)
        # step 3 : find the inner tangent lines intersction point (xi,yi) makesure r1 > r2
        xo = (x2 * r1 + x1 * r2) / (r1 + r2)
        yo = (y2 * r1 + y1 * r2) / (r1 + r2)
        # print(r1,r2,xo,yo)
        # ax2.plot(np.array([x1,x2,xo]),np.array([y1,y2,yo]),'b-')
        # step 4 : calc the inner tangent point xt5,yt5 ... xt8,yt8
        xt5 = (r1 ** 2 * (xo - x1) + r1 * (yo - y1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + x1
        yt5 = (r1 ** 2 * (yo - y1) - r1 * (xo - x1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + y1
        # s = np.round((y1-yt1)*(yo-yt1)/((xt1-x1)*(xt1-xo)))
        xt6 = (r1 ** 2 * (xo - x1) - r1 * (yo - y1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + x1
        yt6 = (r1 ** 2 * (yo - y1) + r1 * (xo - x1) * np.sqrt((xo - x1) ** 2 + (yo - y1) ** 2 - r1 ** 2)) / (
                    (xo - x1) ** 2 + (yo - y1) ** 2) + y1
        # print(xt5,yt5,xt6,yt6,s)
        xt7 = (r2 ** 2 * (xo - x2) + r2 * (yo - y2) * np.sqrt((xo - x2) ** 2 + (yo - y2) ** 2 - r2 ** 2)) / (
                    (xo - x2) ** 2 + (yo - y2) ** 2) + x2
        yt7 = (r2 ** 2 * (yo - y2) - r2 * (xo - x2) * np.sqrt((xo - x2) ** 2 + (yo - y2) ** 2 - r2 ** 2)) / (
                    (xo - x2) ** 2 + (yo - y2) ** 2) + y2
        # ss = np.round((y3-yt3)*(yo-yt3)/((xt3-x3)*(xt3-xo)))
        xt8 = (r2 ** 2 * (xo - x2) - r2 * (yo - y2) * np.sqrt((xo - x2) ** 2 + (yo - y2) ** 2 - r2 ** 2)) / (
                    (xo - x2) ** 2 + (yo - y2) ** 2) + x2
        yt8 = (r2 ** 2 * (yo - y2) + r2 * (xo - x2) * np.sqrt((xo - x2) ** 2 + (yo - y2) ** 2 - r2 ** 2)) / (
                    (xo - x2) ** 2 + (yo - y2) ** 2) + y2

        # print(xt7,yt7,xt8,yt8,ss)
        # step 5 : draw outer and inner tangent lines
        if plotting == 1:
            ax2.plot(np.array([xt1, xt3]), np.array([yt1, yt3]), 'r--', label='outerTangent1')
            ax2.plot(np.array([xt2, xt4]), np.array([yt2, yt4]), 'b--', label='outerTangent2')
            ax2.plot(np.array([xt5, xt7]), np.array([yt5, yt7]), 'g--', label='innerTangent1')
            ax2.plot(np.array([xt6, xt8]), np.array([yt6, yt8]), 'k--', label='innerTangent2')
            ax2.legend()

        line1 = xt1, yt1, xt3, yt3
        line2 = xt2, yt2, xt4, yt4
        line3 = xt5, yt5, xt7, yt7
        line4 = xt6, yt6, xt8, yt8
        tangent.append(line1)
        tangent.append(line2)
        tangent.append(line3)
        tangent.append(line4)
        return tangent


# develop the function to calculate rTrk and chi2
# function to calculate distance to Track y = m*x + b
def dist(x, y, m, b):
    return abs(m * np.array(x) - np.array(y) + b) / math.sqrt(m ** 2 + 1)


# function to convert line (x1,y1,x2,y2) to m,b
def lineConv(line):
    x1, y1, x2, y2 = line
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return m, b


def getMatchedLine(lines, seg, resSigma):
    chi2List = []
    locY, locZ, radial = seg
    for line in lines:
        m, b = lineConv(line)
        rTrk_refit = dist(locY, locZ, m, b)
        residual_new = radial - np.abs(rTrk_refit)
        track_chi2_new = sum((radial - np.abs(rTrk_refit)) ** 2 / resSigma ** 2) / (len(radial) - 1)
        chi2List.append(track_chi2_new)
        # print(line, track_chi2_new)
    index = np.argmin(chi2List)
    return lines[index], chi2List[index]


def refitSegment(x, resolution_constants):
    locY = [float(y) for y in x.mdt_posY[1:-1].split(', ')]
    locZ = [float(y) for y in x.mdt_posZ[1:-1].split(', ')]
    radial = np.abs([float(y) for y in x.mdt_r[1:-1].split(', ')])
    # radial = np.abs([float(y) for y in x.newR[1:-1].split(', ')])

    seg = locY, locZ, np.abs(radial)
    points = list(zip(locY, locZ, np.abs(radial)))
    # print(len(points),len(radial))
    reconPoints = []

    # create resolution function for chi2 calcualtion
    # z=np.array([-0.27691671, 6.43554103, -55.16984486, 240.10554353])
    resSigma = np.polyval(resolution_constants, np.abs(radial)) / 1000.
    # loop all hits and get reconPoints
    best_chi2 = []
    best_line = []
    for n in np.arange(1, len(points)):
        lines = tangentLine(points[n - 1], points[n], 0)
        matchedLine, chi2 = getMatchedLine(lines, seg, resSigma)
        best_chi2.append(chi2)
        best_line.append(matchedLine)
        reconPoints.append(matchedLine)

    x = []
    y = []
    for point in reconPoints:
        x1, y1, x2, y2 = point
        x.append(x1)
        x.append(x2)
        y.append(y1)
        y.append(y2)

    # refit segment hits to new track line
    m_refit, b_refit = np.polyfit(x, y, 1)
    rTrk_refit = dist(locY, locZ, m_refit, b_refit)
    # residual_new = np.abs(radial)- np.abs(rTrk_refit)
    # track_chi2_new = sum((np.abs(radial)-np.abs(rTrk_refit))**2/resSigma**2)/(len(radial)-1)
    return rTrk_refit


# function for residual fit
# Double gaussian with shared mean 0=peak1  1=sigma1  2=mean 3=peak2 4=sigma2
def doubleG_fit(x, peak1, sigma1, mean, peak2, sigma2):
    t = (x - mean) / sigma1
    narrow = peak1 * np.exp(-0.5 * t * t)
    t = (x - mean) / sigma2
    wide = peak2 * np.exp(-0.5 * t * t)
    return narrow + wide


def singleGaussian(x, peak1, sigma1, mean):
    t = (x - mean) / sigma1
    narrow = peak1 * np.exp(-0.5 * t * t)
    return narrow


def fitResidual(x, bins, chamber, axes):
    binwidth = 2000 / len(x)
    # x = np.array(hist.values)
    # var= np.array(hist.variances)
    # bins = np.array(hist.edges)[:-1]+binwidth/2. # get rid of extra bin 'uproot special'
    bins = bins[1:]
    # calculate mean and std for histogram data
    mean = np.average(bins, weights=x)
    std = np.sqrt(np.average((bins - mean) ** 2, weights=x))
    print(mean, std)

    # decide fixed fitting range -1mm to 1mm

    x_min = -1000
    x_max = 1000
    # tuncate the data range to -1mm to 1mm
    # x = np.sum(val,axis=0)[400:600]
    # print(np.amax(np.sum(x,axis=0)))
    # bins = edges[1][400:601]*1000

    # customize label and title
    axes.set_xlabel('Residual [um]', fontsize=15)
    axes.set_title('%s_residual' % chamber, fontsize=15, color='r')

    # plot residual data
    axes.plot(bins + binwidth / 2., x, drawstyle='steps', label='Residual_hist')
    axes.plot(bins, x, 'b.', label='Residual_point')

    # do curve_fit with p0 guessed parameters
    # guess = [139.82120082,  86.97521981,  0 , 59.09768902 ,214.70392356]
    # fun3.SetParameters(ampl,rms/4.,mean,ampl/10.,rms*2) # constant,mean,sigma
    initialGuess = [max(x), std / 2., mean, max(x) / 10, std * 2]
    popt1, pcov1 = curve_fit(doubleG_fit, bins, x, p0=initialGuess, maxfev=10000)
    print('peak1 : %.3f | sigma1 : %.3f | mean : %.3f | peak2 : %.3f | sigma2 : %.3f' % (tuple(popt1)))

    # calculate chi2/ndf
    # remove zero bins to avoid the inf.
    zeroFilter = np.where(x != 0)
    chi2 = np.sum((x[zeroFilter] - doubleG_fit(bins[zeroFilter], *popt1)) ** 2 / x[zeroFilter])
    ndf = len(x[zeroFilter]) - 5
    # chi2 = np.sum((x - doubleG_fit(bins, *popt1))**2/var)
    # ndf = len(x) - 5
    chi2ndf = chi2 / ndf
    print(chi2, ndf, chi2ndf)

    # plot narrow and wide GaussianFitting
    # peak1 : 627.809 | sigma1 : 85.241 | mean : 50.451 | peak2 : 494.648 | sigma2 : 174.630
    peak_n, std_n, mean_n, peak_w, std_w = popt1
    # swap narrow and wide Gaussian peak and sigma
    if np.abs(std_n) > np.abs(std_w):
        tmp = peak_w, std_w
        peak_w, std_w = peak_n, std_n
        peak_n, std_n = tmp
    # draw fitted function
    x_n = np.linspace(-1000, 1000, 200)
    res1 = axes.plot(x_n, doubleG_fit(x_n, *popt1), 'r-', label='DoubleGaussianFitting')
    # y_n =  singleGaussian(x_n,peak_n,np.abs(std_n),mean_n)
    # y_w =  singleGaussian(x_n,peak_w,np.abs(std_w),mean_n)
    # axes.plot(x_n,y_n,'m.',label ='NarrowGaussianFitting' )
    # axes.plot(x_n,y_w,'g.',label ='WideGaussianFitting' )

    # calculate A1/A2 ratio
    ratio = abs(peak_n * std_n / (peak_w * std_w))

    # calculate FWHM sigma
    y = doubleG_fit(bins, *popt1)
    Xmax = np.max(y)
    XmaxIndex = np.argmax(y)
    xlo = np.argmin(np.abs(y[:XmaxIndex] - np.max(y) / 2.))
    # print('before tunning xlo :',xlo)
    if (y[xlo] > Xmax / 2.):
        xlo = xlo - (y[xlo] - Xmax / 2.) / (y[xlo] - y[xlo - 1])
    else:
        xlo = xlo + (Xmax / 2. - y[xlo]) / (y[xlo + 1] - y[xlo])
    # print('after tunning xlo :',xlo)

    xhi = np.argmin(np.abs(y[XmaxIndex:] - np.max(y) / 2.)) + XmaxIndex
    # print('before tunning xhi :',xhi)
    if (y[xhi] > Xmax / 2.):
        xhi = xhi - (y[xhi] - Xmax / 2.) / (y[xhi - 1] - y[xhi])
    else:
        xhi = xhi + (Xmax / 2. - y[xhi]) / (y[xhi] - y[xhi + 1])
    # print('after tunning xhi :',xhi)
    # print(xlo,xhi,xhi-xlo)
    # calculate FWHM sigma
    fwhm = binwidth * (xhi - xlo) / 2.3548
    print("FWHM:{:.3f}".format(fwhm))

    # print the fitting result
    axes.text(-1010, Xmax * 0.52, \
              "Entries = %d\nMean =  %.2f$\mu$m\nStd Dev = %.2f\n-----------------------\npeak1 = %.2f\n$\sigma_1=%.3f\mu$m\npeak2 = %.2f\n$\sigma_2=%.3f\mu$m\n$A_1/A_2=%.3f$\n$\mu=%.3f\mu$m\n$\sigma_\epsilon=%.3f\mu \
               $m\n$\chi^2$/ndf=%.3f" % (
              (np.sum(x)), mean, std, peak_n, abs(std_n), peak_w, abs(std_w), ratio, mean_n, fwhm, chi2ndf), \
              backgroundcolor='linen', fontsize=12)
    axes.legend()
    axes.grid(True)
    return res1, (np.sum(x), mean, std, peak_n, abs(std_n), peak_w, abs(std_w), ratio, mean_n, fwhm, chi2ndf)


# function for T0/Tmax fit
# p0 : pedestal , A0 : amplitude, t0 : t0, T : leading edge slope
# initial parameters p0=[0,np.max(y),0,0.3]
def leadingEdge_func(t, p0, A0, t0, T):
    return p0 + A0 / (1 + np.exp(-(t - t0) / T))


# pmax : pedestal, Amax : strightline intercept, amax : straightLine slope
# tmax : tmax, Tmax : trailing edge slope
# initial parameters sMDT p0=[0,0.5*np.max(y),-2,190,3] , MDT p0=[0,0.5*np.max(y),0,700,3]
def trailEdge_func(t, pmax, Amax, amax, tmax, Tmax):
    return pmax + (Amax + amax * t) / (1 + np.exp((t - tmax) / Tmax))


def fitT0Tmax(df, chamber, axes):
    # set low/high histogram range sMDT [-100,350] ,MDT [-100,800]
    tlow = -100
    thigh = 800
    binsize = 1
    # setup low/high fitting range for T0 and Tmax fit
    t0FitRange = [30, 150]
    # tmaxFitRange = [750,890] # sMDT [250, 310]
    tmaxFitRange = [750, 890]
    if chamber[:3] in ['BMG', 'BME']:
        thigh = 350
        tmaxFitRange = [230, 340]

    # x,bins= np.histogram(df_resi_ex[df_resi_ex['mdt_chamber']==chamber].mdt_t.values.astype(float), bins = np.arange(tlow,thigh,binsize))
    x, bins = np.histogram(df.astype(float), bins=np.arange(tlow, thigh, binsize))

    axes.set_xlabel('DriftTime [ns]', fontsize=12)
    axes.set_title(chamber, fontsize=15, color='r')

    axes.scatter(bins[:-1], x)
    axes.set_ylim([-2, max(x)])

    popt1, pcov1 = curve_fit(leadingEdge_func, bins[t0FitRange[0]:t0FitRange[1]], x[t0FitRange[0]:t0FitRange[1]],
                             p0=[0, np.max(x), 0, 0.3])
    popt2, pcov2 = curve_fit(trailEdge_func, bins[tmaxFitRange[0]:tmaxFitRange[1]], x[tmaxFitRange[0]:tmaxFitRange[1]],
                             p0=[0, 0.5 * np.max(x), 0, np.mean(tmaxFitRange) - 100, 3])

    # print(popt1)
    # print(popt2)
    # print ('p0 : %.3f | A0 : %.3f | t0 : %.3f | t0_slope : %.3f'%(tuple(popt1)))
    # print ('pmax : %.3f | Amax : %.3f | tmax_ped : %.3f | tmax : %.3f | tmax_slope : %.3f'%(tuple(popt2)))
    res1 = axes.plot(bins[t0FitRange[0]:t0FitRange[1]], leadingEdge_func(bins[t0FitRange[0]:t0FitRange[1]], *popt1),
                     'r-', label='LeadingEdgeFitting')
    res2 = axes.plot(bins[tmaxFitRange[0]:tmaxFitRange[1]],
                     trailEdge_func(bins[tmaxFitRange[0]:tmaxFitRange[1]], *popt2), 'b-', label='TrailEdgeFitting')
    axes.text(tmaxFitRange[0] * 0.85, np.max(x) * 0.68,
              'entries : %d\nt0 : %.3f ns\nt0_slope : %.3f\ntmax : %.3f ns\ntmax_slope : %.3f' % (
              np.sum(x), popt1[2], popt1[3], popt2[3], popt2[4]), backgroundcolor='linen')
    axes.legend()
    axes.grid(True)
    return popt1, popt2, axes


# function to fit RT relation and Tube resolution polynomial curve
# no display version
def fitRtRes(rtData):
    df_rt = pd.read_csv(rtData)
    # remove extra spaces and split string content into r,t,rerror columns
    df_rt[['rnp', 'tnp', 'renp']] = df_rt[df_rt.columns[0]].str.strip().str.split(' ', expand=True, n=3)
    rnp, tnp, renp = df_rt.rnp.astype(float), df_rt.tnp.astype(float), df_rt.renp.astype(float)

    # define the splitBin by checking sMDT or MDT chamber
    calibName = rtData.split('/')[-1][3:-4]
    chamberName = chamberlist.MDThardname(chamberlist.MDTindex(calibName))
    splitBin = 13  # sMDT = 25  MDT = 13
    searchMaxRange = 150
    if (chamberName[:3] in ['BME', 'BMG']):
        splitBin = 25
        # searchMaxRange = 100
    splitDriftTime = tnp[splitBin]
    diffJointPoint = -1.

    # fit rt by two polynomial functions
    zl, zl_residuals, _, _, _ = np.polyfit(tnp[splitBin:], rnp[splitBin:], 4, full=True)
    zl_ndf = len(tnp[splitBin:])
    zs, zs_residuals, _, _, _ = np.polyfit(tnp[:splitBin + 1], rnp[:splitBin + 1], 1, full=True)
    zs_ndf = len(tnp[:splitBin + 1])
    # fit resolution by one polynomial function
    z, residuals, _, _, _ = np.polyfit(rnp, renp * 1000.0, 4, full=True)
    ndf = len(rnp)

    # refine splitDriftTime if possible
    # scan splitpoints
    xxx = np.linspace(0, searchMaxRange, 10 * searchMaxRange)
    yyy = np.subtract(np.polyval(zl, xxx), np.polyval(zs, xxx))
    # find the index of change sign element, if no index is found, return the smallest diffJoint
    idx = np.where(yyy[:-1] * yyy[1:] < 0)[0] + 1
    if idx != []:
        splitDriftTime = xxx[idx[0]]
        diffJointPoint = yyy[idx[0]]
    else:
        splitDriftTime = xxx[np.argmin(np.abs(yyy))]
        diffJointPoint = yyy[np.argmin(np.abs(yyy))]
    # print(chamberName,idx,splitDriftTime,diffJointPoint)
    # get residual mean and std for rt and res, also save splitRadius

    return calibName, chamberName, splitDriftTime, diffJointPoint, zs, zs_residuals, zs_ndf, zl, zl_residuals, zl_ndf, z, residuals, ndf


# function to load RT parameters from csv dataframe file
def getRtRes(rtDb, chamber):
    # Draw RT function by loading 'UM6608_RtResFit.csv'
    df_RtResFit = pd.read_csv(rtDb)
    # da = df_RtResFit[df_RtResFit['chamber'] == 'BIL2A01']
    da = df_RtResFit[df_RtResFit['chamber'] == chamber]
    print(da.values)

    zs = np.array([float(x) for x in da.values[0][5][1:-1].split(', ')])
    zl = np.array([float(x) for x in da.values[0][8][1:-1].split(', ')])
    z = np.array([float(x) for x in da.values[0][11][1:-1].split(', ')])
    splitDriftTime = float(da.values[0][3])

    return splitDriftTime, zs, zl, z


def t_to_r(rtDb):
    pass


# draw RT and Resolution functions

def preProcessSegmentHits(pd_event):
    mdt_cols = [x for x in pd_event.columns if x[:4] == 'mdt_']
    for col in mdt_cols:
        if col == 'mdt_rTrk_new': continue
        if col == 'mdt_r': continue

        if col == 'mdt_tubeInfo':
            pd_event[col] = pd_event[col].apply(lambda x: x[1:-1].split(', '))
        else:
            print(col)
            pd_event[col] = pd_event[col].apply(lambda x: [float(y) for y in x[1:-1].split(', ')])

    pd_event_ex = pd.concat([pd_event[i].explode() for i in mdt_cols], axis=1)
    pd_event_ex[['mdt_chamber', 'mdt_ml', 'mdt_ly', 'mdt_tb']] = pd_event_ex['mdt_tubeInfo'].str.strip("\'").str.split(
        '-', expand=True, n=4)

    return pd_event_ex