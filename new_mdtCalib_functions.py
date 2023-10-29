#!/usr/bin/env python
# coding: utf-8
import uproot
import pandas as pd
import sys, os, time, math
import re, glob
import numpy as np
import itertools
import muonfixedid, chamberlist
import splitter_regions_Run2
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
import xMdtSegment as xSeg
import mdtfunctions


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
        if r1 < r2:
            line1 = x2, y2, x1, y1
            line2 = x2, y2, x1, y1
            line3 = x2, y2, x1, y1
            line4 = x2, y2, x1, y1
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
        if r1 < r2:
            line1 = xt3, yt3, xt1, yt1
            line2 = xt4, yt4, xt2, yt2
            line3 = xt7, yt7, xt5, yt5
            line4 = xt8, yt8, xt6, yt6
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
        if r1 < r2:
            line1 = xt3, yt3, xt1, yt1
            line2 = xt4, yt4, xt2, yt2
            line3 = xt7, yt7, xt5, yt5
            line4 = xt8, yt8, xt6, yt6
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
        # reverse point order
        if r1 < r2:
            line1 = xt3, yt3, xt1, yt1
            line2 = xt4, yt4, xt2, yt2
            line3 = xt7, yt7, xt5, yt5
            line4 = xt8, yt8, xt6, yt6
        tangent.append(line1)
        tangent.append(line2)
        tangent.append(line3)
        tangent.append(line4)
        return tangent


# function to convert two points (x1,y1),(x2,y2) to a,b,c
def twoPoints2line(twoPoints):
    x1, y1, x2, y2 = twoPoints
    a = y2 - y1
    b = x1 - x2
    c = a * x1 + b * y1

    return a, b, c


def dist_abc(x, y, a, b, c):
    return np.abs(a * np.array(x) + b * np.array(y) + c) / (np.sqrt(a * a + b * b))


# develop the function to calculate rTrk and chi2
# function to calculate distance to Track y = m*x + b
# adding sign of rTrk by check the function result

def dist_mb(x, y, m, b):
    return abs(m * np.array(x) - np.array(y) + b) / math.sqrt(m ** 2 + 1)


# function to convert line (x1,y1,x2,y2) to m,b
# need to handle x1 == x2 case specially
def lineConv(line):
    x1, y1, x2, y2 = line
    if (x2 == x1):
        m, b = 0.0, 0.0
    else:
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
    return m, b


def getMatchedLine(lines, seg, resSigma):
    chi2List = []
    locY, locZ, radial = seg
    for line in lines:
        m, b = lineConv(line)
        rTrk_refit = dist_mb(locY, locZ, m, b)
        residual_new = np.abs(radial) - np.abs(rTrk_refit)
        track_chi2_new = sum((radial - np.abs(rTrk_refit)) ** 2 / resSigma ** 2) / (len(radial) - 1)
        chi2List.append(track_chi2_new)
        # print(line, track_chi2_new)
    # print (chi2List)
    index = np.argmin(chi2List)
    return lines[index], chi2List[index]


# new matchedLine function
def getCandidateLines(lines, seg, resSigma):
    chi2List = []
    lineList = []
    locY, locZ, radial = seg
    for line in lines:
        m, b = lineConv(line)
        rTrk_refit = dist_mb(locY, locZ, m, b)
        residual_new = radial - np.abs(rTrk_refit)
        track_chi2_new = sum((radial - np.abs(rTrk_refit)) ** 2 / resSigma ** 2) / (len(radial) - 1)
        if track_chi2_new < 500.:
            chi2List.append(track_chi2_new)
            lineList.append(list(line))
        # print(line, track_chi2_new)
    # print (chi2List)
    # index = np.argmin(chi2List)
    return lineList, chi2List
'''
def refitSegment(x, resolution_constants):
    # print(x.event_eventNumber)
    seg = xSeg.xMdtSegment(x)
    flag, track_chi2_new, track_chi2_default, rTrk_new, xline = seg.applyRefitSegment(dist_mbresolution_constants)
    unbias_rTrk_new = seg.applyUnbiasResidual(resolution_constants)

    refit_m, refit_b = xline.getMB()
    # angleYZ = np.rad2deg(np.arctan(m))
    return flag, rTrk_new, track_chi2_new, track_chi2_default, refit_m, refit_b, unbias_rTrk_new

'''

def refitSegment(x, df, resolution_constants):
    # print(x.event_eventNumber)
    seg = xSeg.xMdtSegment(df)
    flag, track_chi2_new, track_chi2_default, rTrk_new, xline = seg.applyRefitSegment(x, resolution_constants)
    unbias_rTrk_new = seg.applyUnbiasResidual(x, resolution_constants)

    refit_m, refit_b = xline.getMB()
    # angleYZ = np.rad2deg(np.arctan(m))
    return flag, rTrk_new, track_chi2_new, track_chi2_default, refit_m, refit_b, unbias_rTrk_new


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


# fit residual without display option
def fitResidualFast(x, bins, chamber):
    # x,bins = np.histogram(df.astype('float')*1000,bins = np.arange(-1000,1000,10))
    binwidth = 2000 / len(x)
    bins = bins[1:]
    # calculate mean and std for histogram data
    mean = np.average(bins, weights=x)
    std = np.sqrt(np.average((bins - mean) ** 2, weights=x))

    # decide fixed fitting range -1mm to 1mm
    x_min = -1000
    x_max = 1000

    # do curve_fit with p0 guessed parameters
    # guess = [139.82120082,  86.97521981,  0 , 59.09768902 ,214.70392356]
    # fun3.SetParameters(ampl,rms/4.,mean,ampl/10.,rms*2) # constant,mean,sigma
    initialGuess = [max(x), std / 2., mean, max(x) / 10, std * 2]
    popt1, pcov1 = curve_fit(doubleG_fit, bins, x, p0=initialGuess, maxfev=20000)
    # print ('peak1 : %.3f | sigma1 : %.3f | mean : %.3f | peak2 : %.3f | sigma2 : %.3f'%(tuple(popt1)))
    # calculate chi2/ndf
    # remove zero bins to avoid the inf.
    zeroFilter = np.where(x != 0)
    chi2 = np.sum((x[zeroFilter] - doubleG_fit(bins[zeroFilter], *popt1)) ** 2 / x[zeroFilter])
    ndf = len(x[zeroFilter]) - 5
    chi2ndf = chi2 / ndf

    # plot narrow and wide GaussianFitting
    # peak1 : 627.809 | sigma1 : 85.241 | mean : 50.451 | peak2 : 494.648 | sigma2 : 174.630
    peak_n, std_n, mean_n, peak_w, std_w = popt1
    # swap narrow and wide Gaussian peak and sigma
    if np.abs(std_n) > np.abs(std_w):
        tmp = peak_w, std_w
        peak_w, std_w = peak_n, std_n
        peak_n, std_n = tmp

    # calculate A1/A2 ratio
    ratio = abs(peak_n * std_n / (peak_w * std_w))

    # calculate sigma
    sigma = (peak_n * abs(std_n) + peak_w * abs(std_w)) / (peak_n + peak_w)

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

    # calculate FWHM sigma
    fwhm = binwidth * (xhi - xlo) / 2.3548

    print('np.sum(x): {}, mean: {}, std: {}, peak_n: {}, abs(std_n): {}, peak_w: {}, abs(std_w): {}, ratio: {}, mean_n: {}, sigma: {}, fwhm: {}, chi2ndf: {}'.format(np.sum(x), mean, std, peak_n, abs(std_n), peak_w, abs(std_w), ratio, mean_n, sigma, fwhm, chi2ndf))

    return (np.sum(x), mean, std, peak_n, abs(std_n), peak_w, abs(std_w), ratio, mean_n, sigma, fwhm, chi2ndf)


def fitResidual(x, bins, chamber, axes):
    # x,bins = np.histogram(df.astype('float')*1000,bins = np.arange(-1000,1000,10))
    binwidth = 2000 / len(x)
    # x = np.array(hist.values)
    # var= np.array(hist.variances)
    # bins = np.array(hist.edges)[:-1]+binwidth/2. # get rid of extra bin 'uproot special'
    bins = bins[1:]
    # calculate mean and std for histogram data
    mean = np.average(bins, weights=x)
    std = np.sqrt(np.average((bins - mean) ** 2, weights=x))
    print('mean : ', mean, 'std : ', std)

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
    popt1, pcov1 = curve_fit(doubleG_fit, bins, x, p0=initialGuess, maxfev=20000)
    # print ('peak1 : %.3f | sigma1 : %.3f | mean : %.3f | peak2 : %.3f | sigma2 : %.3f'%(tuple(popt1)))

    # calculate chi2/ndf
    # remove zero bins to avoid the inf.
    zeroFilter = np.where(x != 0)
    chi2 = np.sum((x[zeroFilter] - doubleG_fit(bins[zeroFilter], *popt1)) ** 2 / x[zeroFilter])
    ndf = len(x[zeroFilter]) - 5
    # chi2 = np.sum((x - doubleG_fit(bins, *popt1))**2/var)
    # ndf = len(x) - 5
    chi2ndf = chi2 / ndf
    # print(chi2,ndf, chi2ndf)

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
    # calculate sigma
    sigma = (peak_n * abs(std_n) + peak_w * abs(std_w)) / (peak_n + peak_w)

    Xmax = np.max(x)
    #
    # calculate FWHM sigma
    y = doubleG_fit(bins, *popt1)
    # Xmax = np.max(y)
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
    # print("FWHM:{:.3f}".format(fwhm))

    # print the fitting result
    axes.text(-1010, Xmax * 0.52, \
              "Entries = %d\nMean =  %.2f$\mu$m\nStd Dev = %.2f\n-----------------------\npeak1 = %.2f\n$\sigma_1=%.3f\mu$m\npeak2 = %.2f\n$\sigma_2=%.3f\mu$m\n$A_1/A_2=%.3f$\n$\mu=%.3f\mu$m\n$\sigma_{aw}=%.3f\mu$m\n$\sigma_{fwhm}=%.3f\mu \
               $m\n$\chi^2$/ndf=%.3f" % (
              (np.sum(x)), mean, std, peak_n, abs(std_n), peak_w, abs(std_w), ratio, mean_n, sigma, fwhm, chi2ndf), \
              backgroundcolor='linen', fontsize=12)
    axes.legend()
    axes.grid(True)
    return res1, (
    np.sum(x), mean, std, peak_n, abs(std_n), peak_w, abs(std_w), ratio, mean_n, sigma, fwhm, chi2ndf), axes


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


# p1 : pedestal, p2,p3,p4 middle shape, p5 : t0 , p6 : tmax, p7 : t0slope, p8 : tmaxslope
# initial parameters sMDT pinit=[0,0.3*np.max(x),10000,100,0,np.mean(tmaxFitRange)-100,3,7], MDT pinit = [0,0.3*np.max(x),5,220,0,np.mean(tmaxFitRange)-100,3,7]
def driftTimeFitting_func(t, par1, par2, par3, par4, par5, par6, par7, par8):
    # return par[0]+ (par[1]*(1+par[2]*np.exp(-(t-par[4])/par[3])))/((1+np.exp(-(t-par[4])/par[6]))*(1+np.exp((t-par[5])/par[7])))
    return par1 + (par2 * (1 + par3 * np.exp(-(t - par5) / par4))) / (
                (1 + np.exp(-(t - par5) / par7)) * (1 + np.exp((t - par6) / par8)))


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

    axes.scatter(bins[:-1], x, s = 4)
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
                     'r-', label='LeadingEdgeFitting', markersize = 4)
    res2 = axes.plot(bins[tmaxFitRange[0]:tmaxFitRange[1]],
                     trailEdge_func(bins[tmaxFitRange[0]:tmaxFitRange[1]], *popt2), 'b-', label='TrailEdgeFitting', markersize = 4)
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

    zs = np.array([float(x) for x in da.values[0][5][1:-1].split(', ')])
    zl = np.array([float(x) for x in da.values[0][8][1:-1].split(', ')])
    z = np.array([float(x) for x in da.values[0][11][1:-1].split(', ')])
    splitDriftTime = float(da.values[0][3])

    return splitDriftTime, zs, zl, z


def t_to_r(rtDb):
    pass


# draw RT and Resolution functions

# preProcess segment hits
def preProcessSegmentHits(pd_event):
    mdt_cols = [x for x in pd_event.columns if x[:4] == 'mdt_']
    for col in mdt_cols:
        if col == 'mdt_rTrk_new': continue
        if col == 'mdt_rTrk_unbias': continue

        # if col == 'mdt_r' : continue

        if col == 'mdt_tubeInfo':
            pd_event[col] = pd_event[col].apply(lambda x: x[1:-1].split(', '))
        else:
            # print(col)
            pd_event[col] = pd_event[col].apply(lambda x: [float(y) for y in x[1:-1].split(', ')])

    pd_event_ex = pd.concat([pd_event[i].explode() for i in mdt_cols], axis=1)
    pd_event_ex[['mdt_chamber', 'mdt_ml', 'mdt_ly', 'mdt_tb']] = pd_event_ex['mdt_tubeInfo'].str.strip("\'").str.split(
        '-', expand=True, n=4)

    return pd_event_ex


# function to flatten string array to np.array(float)
def stringFlatten(df):
    return np.hstack(np.array([[float(st) for st in item.strip('[]\s').split(',')] for item in list(df.values)]))


############################
### draw histograms function
############################
def drawSegmentPlots(pd_event, run, chamberName):
    # make chamber segment level overall plots
    fig, axes = plt.subplots(figsize=(30, 17), nrows=2, ncols=3)
    fig.subplots_adjust(top=0.93, bottom=0.05, left=0.02, right=0.98, wspace=0.2, hspace=0.2)
    fig.suptitle('run%s_%s_segmentPlots' % (run, chamberName), fontsize=20)

    # segment nHits
    mdt_nHits = pd_event.seg_nMdtHits.values.astype(int)
    axes[0, 0].hist(mdt_nHits, bins=np.max(mdt_nHits), range=[0, np.max(mdt_nHits)], label='segment nHits')
    axes[0, 0].set_xlabel('#hits per segment')

    # segment chi2
    mdt_chi2 = pd_event.seg_chi2_new.values.astype(float)
    axes[0, 1].hist(mdt_chi2, bins=30, range=[0, 60], label='segment chi2')
    axes[0, 1].legend()
    axes[0, 1].set_xlabel('segment chi2')

    # segment quality
    mdt_quality = pd_event.seg_quality.values.astype(int)
    text = '100*#Holes \n10*#Out-of-time hits \n1*Delta hits'
    axes[0, 2].hist(mdt_quality, bins=10, range=[0, 1000], label=text)
    axes[0, 2].set_xlabel('segment quality')
    axes[0, 2].legend()

    # segment angleYZ
    dirx = pd_event.seg_dirX.values.astype(float)
    diry = pd_event.seg_dirY.values.astype(float)
    dirz = pd_event.seg_dirZ.values.astype(float)

    beta = np.rad2deg(np.arctan2(diry, dirz))
    axes[1, 1].hist(beta, bins=90, range=[-90, 90], label='segment inclination angle YZ')
    axes[1, 1].set_xlabel('segment angle of inclination localYZ [degree]')

    # segment angleZX
    alpha = np.rad2deg(np.arctan2(dirz, dirx))
    axes[1, 0].hist(alpha, bins=90, range=[0, 180], label='segment inclination angle YZ')
    axes[1, 0].set_xlabel('segment angle of inclination localZX [degree]')

    # segment fitted angleYZ - default angleYZ
    # refit_angle = np.rad2deg(np.arctan(1/pd_event.seg_refitSlope))
    # axes[1,2].hist( refit_angle - beta, bins =100, range = [-5, 5],label = 'segment inclination angle YZ (refit-default)' )
    # axes[1,2].set_xlabel('refit-default segment inclination angle localYZ [degree]')

    pt = pd_event.seg_Pt.values.astype(int)
    axes[1, 2].hist(pt, bins=100, range=[0, 200], label='segment Pt[GeV]')
    axes[1, 2].set_xlabel('segment Pt[GeV]')

    print('save plots to run%s_%s_segmentPlots_overall.png' % (run, chamberName))
    plt.savefig('run%s_%s_segmentPlots_overall.png' % (run, chamberName))

    return axes


# compare chi2

def drawChi2(pd_event, run, chamberName):
    # run = pd_event.event_runNumber[0]

    fig, axes = plt.subplots(figsize=(20, 8), ncols=2)
    fig.subplots_adjust(top=0.94, bottom=0.04, left=0.02, right=0.98, wspace=0.2, hspace=0.2)
    fig.suptitle('run%s_%s_segmentPlots_refitChi2' % (run, chamberName), fontsize=20)

    mdt_chi2 = pd_event.seg_chi2_def.astype(float)
    mdt_chi2_new = pd_event.seg_chi2_new.astype(float)
    x = mdt_chi2
    y = mdt_chi2_new
    d = np.array(x) - np.array(y)
    # print(len(x),len(y),len(d))
    x_w = np.empty(x.shape)
    x_w.fill(1 / x.shape[0])
    y_w = np.empty(y.shape)
    y_w.fill(1 / y.shape[0])
    # bins = np.linspace(0, 18, 18)
    axes[0].hist([x, y], bins=np.arange(-0.5, 59.5, 5), range=[0, 60], weights=[x_w, y_w], alpha=0.6,
                 label=['defaultSegment_chi2', 'refitSegment_chi2'])
    axes[0].legend(loc='upper right')
    axes[0].set_xticks(np.arange(0, 60, step=5))
    axes[0].set_xlabel('segment chi2')
    axes[0].set_ylabel('normalized rate')

    # print difference between oldChi2 and newChi2
    xd, xdbins, dpatch = axes[1].hist(d, bins=100, range=[-50, 50], label='Delta Chi2')
    # mean = np.mean(d)
    # std = np.sqrt(np.average((d - mean)**2))
    # #axes[1,0].set_xlim(50,350)
    axes[1].set_xlabel('default_Chi2 - refitted_Chi2', fontsize=15)
    # axes[1].text(30,np.max(xd)*0.82,'Entries : %d\nMean : %.3f\nStd Dev : %.3f'%(np.sum(d),mean,std),backgroundcolor='linen',fontsize =13)
    axes[1].grid()

    print('save plots to run%s_%s_segmentPlots_refitChi2.png' % (run, chamberName))
    plt.savefig('run%s_%s_segmentPlots_refitChi2.png' % (run, chamberName))

    return axes


# function to convert single columns string data to np.array
def conv(df):
    return np.hstack(np.array([[float(st) for st in item.strip('[]\s').split(',')] for item in list(df.values)]))
    # return np.hstack(np.array([[float(st) for st in item[2:-2].split()] for item in list(df.values)]))  # for DESD data


def drawResidual(df_segHit, run, chamberName):
    # make chamber overall info
    # run = df_segHit.event_runNumber

    fig, axes = plt.subplots(figsize=(30, 17), nrows=2, ncols=3)
    fig.subplots_adjust(top=0.93, bottom=0.05, left=0.02, right=0.98, wspace=0.2, hspace=0.2)
    fig.suptitle('run%s_%s_chamberPlots' % (run, chamberName), fontsize=20)

    mdt_r = conv(df_segHit.mdt_r)
    # mdt_adc = df_segHit.mdt_adc.astype(float)
    # mdt_r = df_segHit.mdt_r
    mdt_t = conv(df_segHit.mdt_t)
    mdt_rTrk = conv(df_segHit.mdt_rTrk)
    mdt_rTrk_new = conv(df_segHit.mdt_rTrk_new)
    mdt_rTrk_unbias = conv(df_segHit.mdt_rTrk_unbias)

    # driftTime spectrum
    t0_fit, tmax_fit, axes[0, 0] = fitT0Tmax(mdt_t, chamberName, axes[0, 0])

    # ADC count
    mdt_adc = conv(df_segHit.mdt_adc)
    xadc, xbins, patch = axes[1, 0].hist(mdt_adc, bins=75, range=[50, 350], label='adc')
    mean = np.average(mdt_adc)
    std = np.sqrt(np.average((mdt_adc - mean) ** 2))
    axes[1, 0].set_xlim(50, 350)
    axes[1, 0].set_xlabel('adcCount', fontsize=15)
    axes[1, 0].text(270, np.max(xadc) * 0.82,
                    'Entries : %d\nMean : %.3f ns\nStd Dev : %.3f' % (np.sum(xadc), mean, std), backgroundcolor='linen',
                    fontsize=13)
    axes[1, 0].grid()

    # RT function
    maxRadius, maxDriftTime = 15.0, 800.0
    # splitBin = 13  # sMDT = 25  MDT = 13
    if (chamberName[:3] in ['BME', 'BMG']):
        maxRadius, maxDriftTime = 7.5, 200.0
    # rtData = '../UM6608/Rt_BMG_6_-2.dat'

    # residual
    mdt_resi_new = np.abs(mdt_r) - np.abs(mdt_rTrk_new)
    mdt_resi_unbias = np.abs(mdt_r) - np.abs(mdt_rTrk_unbias)

    # mdt_resi = df_segHit.mdt_resi.values.astype(float)
    x1, bins1 = np.histogram(mdt_resi_unbias * 1000, bins=np.arange(-1000, 1000, 10))
    x0, bins0 = np.histogram(mdt_resi_new * 1000, bins=np.arange(-1000, 1000, 10))

    fitResidual(x1, bins1, 'Residual_unbias', axes[0, 2])
    fitResidual(x0, bins0, 'Residual_bias', axes[0, 1])

    counts, xedges, yedges, im2 = axes[1, 1].hist2d(mdt_r, mdt_resi_new, bins=[150, 100],
                                                    range=[[-1 * maxRadius, 1 * maxRadius], [-1, 1]], cmap=plt.cm.BuGn,
                                                    label='residual_vs_radius')
    # cmap.set_bad('white',1.)
    axes[1, 1].set_ylim(-1, 1)
    axes[1, 1].set_xlim(-maxRadius, maxRadius)
    axes[1, 1].set_xlabel('radius [mm]', fontsize=15)
    axes[1, 1].set_ylabel('residual [mm]', fontsize=15)
    # plt.colorbar(im2, ax=axes[1,1])
    # bin_means, bin_edges, binnumber = stats.binned_statistic(mdt_r, mdt_resi, statistic='median', bins=150)
    bin_means_new, bin_edges_new, binnumber_new = stats.binned_statistic(mdt_r, mdt_resi_new, statistic='median',
                                                                         bins=30)

    # axes[1,2].hlines(bin_means, bin_edges[:-1], bin_edges[1:], colors='b', lw=3,label='Default avr<residual>_vs_radius')
    axes[1, 1].hlines(bin_means_new, bin_edges_new[:-1], bin_edges_new[1:], colors='r', lw=3,
                      label='Bias avr<residual>_vs_radius')

    axes[1, 1].legend()
    axes[1, 1].grid()

    counts, xedges, yedges, im2 = axes[1, 2].hist2d(mdt_r, mdt_resi_unbias, bins=[150, 100],
                                                    range=[[-1 * maxRadius, 1 * maxRadius], [-1, 1]], cmap=plt.cm.BuGn,
                                                    label='residual_vs_radius')
    # cmap.set_bad('white',1.)
    axes[1, 2].set_ylim(-1, 1)
    axes[1, 2].set_xlim(-7.5, 7.5)
    axes[1, 2].set_xlabel('radius [mm]', fontsize=15)
    axes[1, 2].set_ylabel('residual [mm]', fontsize=15)
    bin_means_def, bin_edges_def, binnumber_def = stats.binned_statistic(mdt_r, mdt_resi_unbias, statistic='median',
                                                                         bins=30)
    # bin_means_def, bin_edges_def, binnumber_def = stats.binned_statistic(mdt_r, mdt_resi, statistic='std', bins=30)

    # plt.colorbar(im2, ax=axes[1,1])
    # bin_means, bin_edges, binnumber = stats.binned_statistic(mdt_r, mdt_resi, statistic='median', bins=150)
    axes[1, 2].hlines(bin_means_def, bin_edges_def[:-1], bin_edges_def[1:], colors='k', lw=3,
                      label='Unbias avr<residual>_vs_radius')
    axes[1, 2].legend()
    axes[1, 2].grid()

    print('save plots to run%s_%s_chamberPlots_refitResidual.png' % (run, chamberName))
    plt.savefig('run%s_%s_chamberPlots_refitResidual.png' % (run, chamberName))

    return axes


# function to convert RT paraments
def convertRtConstants(da):
    zs = np.array([float(x) for x in da.values[0][5][1:-1].split(', ')])
    zl = np.array([float(x) for x in da.values[0][8][1:-1].split(', ')])
    z = np.array([float(x) for x in da.values[0][11][1:-1].split(', ')])
    splitDriftTime = float(da.values[0][3])
    diffJointPoint = float(da.values[0][4])
    return zs, zl, z, splitDriftTime, diffJointPoint


# Efficiency plots
def drawEfficiency(df, run, chamber, chi2cut, resolution_constants):
    # load data columns
    unbias = df.mdt_rTrk_unbias
    new = df.mdt_rTrk_new
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

    # calculate resolution for each hits
    resSigma = np.polyval(resolution_constants, np.abs(f_new)) / 1000.
    print(resSigma)

    # create a new dataframe for calcuating efficiency
    df_eff = pd.DataFrame({'radius': f_r, 'rTrk_new': f_new, 'rTrk_unbias': f_unbias, 'res_Sigma': resSigma,
                           'resi_unbias': np.abs(resi_unbias)})
    print(df_eff.shape)

    df_eff['sigma3_flag'] = df_eff.apply(check_3sigma, axis=1)
    df_eff['sigma5_flag'] = df_eff.apply(check_5sigma, axis=1)
    df_eff['sigmaHardware_flag'] = df_eff.apply(check_hardware, axis=1)

    df_eff.head()

    # set radius interval
    startSlice = np.arange(0.1, maxRadius, step)
    stopSlice = np.append(startSlice[1:], maxRadius)
    branchBasket = list(zip(*(startSlice, stopSlice)))

    n3_eff = []
    n5_eff = []
    h_eff = []
    for n in range(len(branchBasket)):
        radius_filter = (df_eff.rTrk_new < branchBasket[n][1]) & (df_eff.rTrk_new > branchBasket[n][0])
        count3 = df_eff.sigma3_flag[radius_filter]
        # print(n,len(count3),np.sum(count3))
        n3_eff.append(100.0 * np.sum(count3) / len(count3))
        count5 = df_eff.sigma5_flag[radius_filter]
        n5_eff.append(100.0 * np.sum(count5) / len(count5))
        count_h = df_eff.sigmaHardware_flag[radius_filter]
        # print(n,len(count),np.sum(count))
        h_eff.append(100.0 * np.sum(count_h) / len(count_h))

    print(n3_eff, n5_eff, h_eff)

    # plot eff sigma3, sigma5, hardware
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(top=0.93, bottom=0.05, left=0.02, right=0.98, wspace=0.2, hspace=0.2)

    ax.plot(np.arange(15), h_eff, 'bo', label='Hardware Efficiency')
    ax.plot(np.arange(15), n5_eff, 'rs', label='5 Sigma Efficiency')
    ax.plot(np.arange(15), n3_eff, 'g^', label='3 Sigma Efficiency')

    ax.set_ylabel('Efficiency %', fontsize=15)
    ax.set_xlabel('Raidus [mm]', fontsize=15)
    ax.set_ylim(50, 105)
    ax.set_yticks(np.arange(50, 101, step=5))

    ax.grid()
    ax.legend(fontsize=20)
    plt.suptitle('Run%s_%s_Efficiency_chi2cut%s' % (run, chamber, minChi2), fontsize=20)

    plt.savefig('Run%s_%s_Efficiency_chi2cut%d.png' % (run, chamber, minChi2))


# function to plot the resolution
def plotResolution(df, chamber):
    # load df and prepare the data array
    unbias = df.unbias_rTrk_new
    new = df.rTrk_new
    #new = df.mdt_rTrk
    r = df.mdt_r

    f_r = mdtfunctions.conv(r)
    f_unbias = mdtfunctions.conv(unbias)
    f_new = mdtfunctions.conv(new)

    # for DESD data
    # f_r = np.hstack(np.array([[float(st) for st in item[1:-1].split()] for item in list(r)]))
    # f_new = np.hstack(np.array([[float(st) for st in item[1:-1].split()] for item in list(new)]))
    # f_unbias = np.hstack(np.array([[float(st) for st in item[1:-1].split()] for item in list(unbias)]))

    # get the residual array
    resi_new = np.abs(f_r) - np.abs(f_new)
    resi_unbias = np.abs(f_r) - np.abs(f_unbias)
    resi_def = mdtfunctions.conv(df.mdt_resi)

    print('lengths of resi_def uncut: ', len(resi_def))

    # fit chamber reisudal and calculate chamber R = sqrt(bias*unbias)
    # x,bins = np.histogram(f_resi*1000,bins = np.arange(-1000,1000,20))
    # mdtCalib_functions.fitResidualFast(x,bins,chamber)
    x, bins = np.histogram(resi_new * 1000, bins=np.arange(-1000, 1000, 20))
    fit_bias = fitResidualFast(x, bins, chamber)

    x, bins = np.histogram(resi_unbias * 1000, bins=np.arange(-1000, 1000, 20))
    fit_unbias = fitResidualFast(x, bins, chamber)

    sigma_fit = fit_bias[9]
    sigma_hit = fit_unbias[9]
    R = np.sqrt(sigma_fit * sigma_hit)
    res_chamber = sigma_fit, sigma_hit, R
    print("sigma_fit", "sigma_hit", "R")
    print(sigma_fit, sigma_hit, R)

    # fit residual in radius slice
    maxRadius, maxDriftTime, step, npad = 14.6, 800.0, 1, 16
    # splitBin = 13  # sMDT = 25  MDT = 13
    if (chamber[:3] in ['BME', 'BMG']):
        maxRadius, maxDriftTime, step, npad = 7.1, 200.0, 1, 8

    # test radius slice filter
    startSlice = np.arange(0.1, maxRadius, step)
    stopSlice = np.append(startSlice[1:], maxRadius)
    # startSlice+=1
    # startEvt[0] =0
    branchBasket = list(zip(*(startSlice, stopSlice)))
    # print(branchBasket)
    print('len of branchBasket: ', len(branchBasket))
    def_w = []
    bias_w = []
    unbias_w = []
    for n in range(len(branchBasket)):
        radius_filter = (f_new < branchBasket[n][1]) & (f_new > branchBasket[n][0])
        print('lengths of resi_def : ', len(resi_def[radius_filter]), 'cut number: ', n)
        x, bins = np.histogram(resi_def[radius_filter] * 1000, bins=np.arange(-1000, 1000, 20))
        fit_result = fitResidualFast(x, bins, chamber)
        # print(n,fit_result[1][8],fit_result[1][9])
        def_w.append(fit_result[9])

        x1, bins1 = np.histogram(resi_new[radius_filter] * 1000, bins=np.arange(-1000, 1000, 20))
        fit_result1 = fitResidualFast(x1, bins1, chamber)
        # print(n,fit_result[1][8],fit_result[1][9])
        bias_w.append(fit_result1[9])

        x2, bins2 = np.histogram(resi_unbias[radius_filter] * 1000, bins=np.arange(-1000, 1000, 20))
        fit_result2 = fitResidualFast(x2, bins2, chamber)
        # print(n,fit_result2[1][8],fit_result2[1][9])
        unbias_w.append(fit_result2[9])

    res = np.sqrt(np.array(bias_w) * np.array(unbias_w))

    return res_chamber, res, def_w, bias_w, unbias_w


# function to draw reference resolution plots
def drawReferenceRtResolution(ax, chamber):
    # draw reference resolution
    df_RtResFit = pd.read_csv('UM6608_RtResFit.csv')
    df_RtResFit_old = pd.read_csv('UM5666_RtResFit.csv')
    # referenceChamber = 'EEL1A01'
    maxR = 15
    if chamber[:3] in ['BMG', 'BME']:
        #        referenceChamber = 'BME4A13'
        maxR = 7.5
    MDT_new = df_RtResFit[df_RtResFit['chamber'] == chamber]
    MDT_old = df_RtResFit_old[df_RtResFit_old['chamber'] == chamber]
    MDT_newConstants = convertRtConstants(MDT_new)
    MDT_oldConstants = convertRtConstants(MDT_old)

    xxx = np.linspace(0, maxR, 1000)
    res_new = ax.plot(xxx, np.polyval(MDT_newConstants[2], xxx), color='red', lw = 1)
    #res_old = ax.plot(xxx, np.polyval(MDT_oldConstants[2], xxx))

    return res_new


def drawResolution(df, run, chamber):
    # df.columns
    unbias = df.unbias_rTrk_new
    new = df.rTrk_new
    #new = df.mdt_rTrk
    r = df.mdt_r
    # resi = df.mdt_resi
    # resi = conv(temp_df.mdt_resi)

    f_unbias = mdtfunctions.conv(unbias)
    f_new = mdtfunctions.conv(new)
    f_r = mdtfunctions.conv(r)
    # f_resi = conv(resi)
    resi = np.abs(f_r) - np.abs(f_new)
    resi_new = np.abs(f_r) - np.abs(f_new)
    print('sus resi_new: ', resi_new)
    print('len of resi_new: ', len(resi_new))
    print('sus resi_new times 1000: ', resi_new * 1000)
    print('len of resi_new times 1000: ', len(resi_new * 1000))
    resi_unbias = np.abs(f_r) - np.abs(f_unbias)

    fig = plt.subplots(figsize=(32, 17))
    plt.subplots_adjust(top=0.93, bottom=0.05, left=0.02, right=0.98, wspace=0.2, hspace=0.2)
    grid = plt.GridSpec(2, 3, wspace=0.2, hspace=0.2)
    ax1 = plt.subplot(grid[0, 0])
    ax2 = plt.subplot(grid[1, 0])
    ax = plt.subplot(grid[0:, 1:])

    x, bins = np.histogram(resi_new * 1000, bins=np.arange(-1000, 1000, 20))
    _, fit_bias, _ = fitResidual(x, bins, chamber, ax1)
    ax1.set_title('%s Bias_residual(Fit residual)' % chamber)

    x, bins = np.histogram(resi_unbias * 1000, bins=np.arange(-1000, 1000, 20))
    _, fit_unbias, _ = fitResidual(x, bins, chamber, ax2)
    ax2.set_title('%s Unbias_residual(Hit residual)' % chamber)

    if df.shape[0] > 0:
        res_chamber, resolution, def_w, bias_w, unbias_w = plotResolution(df, chamber)
        print(resolution, def_w, bias_w, unbias_w)

        # if resolution == 0 : continue
        # plot rt function legend
        maxRadius, step = 14.6, 1
        if (chamber[:3] in ['BME', 'BMG']):
            maxRadius, step = 7.1, 1
        res = np.sqrt(np.array(bias_w) * np.array(unbias_w))

        ax.plot(np.arange(0.1 + step / 2., maxRadius + step / 2., step), resolution, 'r*',
                label='%s sqrt(bias*unbias)' % chamber)
        ax.plot(np.arange(0.1 + step / 2., maxRadius + step / 2., step), resolution, 'r-')
        # ax.plot(np.arange(0.1+step/2.,maxRadius+step/2.,step),def_w,'m*',label='%s default bias'%chamber)
        # ax.plot(np.arange(0.1+step/2.,maxRadius+step/2.,step),def_w,'m-')
        #ax.plot(np.arange(0.1 + step / 2., maxRadius + step / 2., step), bias_w, 'b*', label='%s refit bias' % chamber)
        #ax.plot(np.arange(0.1 + step / 2., maxRadius + step / 2., step), bias_w, 'b-')
        #ax.plot(np.arange(0.1 + step / 2., maxRadius + step / 2., step), unbias_w, 'g*',
                #label='%s refit unbias' % chamber)
        #ax.plot(np.arange(0.1 + step / 2., maxRadius + step / 2., step), unbias_w, 'g-')

        ax.set_ylabel('Resolution(sqrt(bias*unbias)) [um]', fontsize=15)
        ax.set_xlabel('Raidus [mm]', fontsize=15)

        label = '$\sigma_{fit}=%.3f\mu$m $\sigma_{hit}=%.3f\mu$m R=%.3f$\mu$m' % (
        res_chamber[0], res_chamber[1], res_chamber[2])
        ax.text(maxRadius * 0.5, 260, label, backgroundcolor='linen', fontsize=20)
        res_new = drawReferenceRtResolution(ax, chamber)

        ax.set_ylim(0, 350)
        ax.grid()
        ax.legend(fontsize=20)
        plt.suptitle('Run%s_%s_Resolution' % (run, chamber), fontsize=20)

        plt.savefig('Run%s_Resolution_%s_newResRefit_1Segment' % (run, chamber))

        plt.show()

    return
