import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge, Polygon
import mdtCalib_functions
import itertools
import xStraightLine as xSL


class xMdtSegment:
    '''load csv pandas dataframe
    author : zhen.yan@cern.ch
    method :
        info() -> summary segment info
        display() -> display segment into matplotlib ax
        refit() -> refit segment and update rTrk and resi columns
    '''

    def __init__(self, df):
        self.df = df
        self.chamber = df.chamber[0].strip('[]\s').split(',')[0].replace("'", "")
        self.nHits = df.seg_nMdtHits
        self.hits = df.mdt_r, df.mdt_posY, df.mdt_posZ
        self.resolution_constants = self.setResolutionConstants()

        # self.fig = fig
        # self.ax = ax

    def info(self):
        # self.chamber = df.seg_station
        # self.nHit = df.seg_nMdtHits
        # self.hits = df.mdt_r,df.mdt_posY,mdt_posZ
        print(self.chamber, self.nHits, self.hits)

    def setResolutionConstants(self):
        resolutionConstants = 0
        if self.df.chamber[0].strip('[]\s').split(',')[0].replace("'", "")[:3] == ['BMG', 'BME']:
            resolutionConstants = np.array(
                [9.93822651e-03, -4.30837625e-01, 7.21167781e+00, -5.65253940e+01, 2.40581782e+02])
        else:
            resolutionConstants = np.array(
                [9.32631545e-03, -4.09630503e-01, 7.00108592e+00, -5.58254861e+01, 2.40028281e+02])
        return resolutionConstants

    def printRange(self):
        locY = [float(y) for y in self.df.mdt_posY[1:-1].split(', ')]
        locZ = [float(y) for y in self.df.mdt_posZ[1:-1].split(', ')]

        return locY, locZ

    # # info flag to display segment info
    # def refitSegment_v2(self, ax, resolution_constants):
    #     # next implement the hit map
    #     locY = [float(y) for y in self.df.mdt_posY[1:-1].split(', ')]
    #     locZ = [float(y) for y in self.df.mdt_posZ[1:-1].split(', ')]
    #     radial = np.abs([float(y) for y in self.df.mdt_r[1:-1].split(', ')])
    #     rTrk = [float(y) for y in self.df.mdt_rTrk[1:-1].split(', ')]

    #     #radial = np.abs([float(y) for y in x.newR[1:-1].split(', ')])

    #     # construct seg and hit points
    #     seg = locY,locZ,np.abs(radial)
    #     points = list(zip(locY,locZ,np.abs(radial)))
    #     #print(len(points),points)
    #     reconPoints = []

    #     # create resolution function for chi2 calcualtion
    #     #resolution_constants=np.array([-0.27691671, 6.43554103, -55.16984486, 240.10554353])
    #     #z=np.array([-0.27691671, 6.43554103, -55.16984486, 240.10554353])
    #     resSigma = np.polyval(resolution_constants,np.abs(radial))/1000.

    #     # loop all hits and get reconPoints
    #     best_chi2 = 100.
    #     cand_chi2 = []
    #     cand_line = []
    #     all_chi2 = []
    #     all_mbList = []
    #     for n in np.arange(1,len(points)) :
    #         lines = mdtCalib_functions.tangentLine(points[n-1],points[n],0)
    #         chi2List = []
    #         lineList = []
    #         for line in lines :
    #             # lline = []
    #             # lline.append(line)
    #             # xline = xSL.xStraightLine(line)
    #             # m_refit,b_refit = xline.mb
    #             # rTrk_refit,track_chi2_new = xline.dist2line(seg,resSigma)
    #             m_refit,b_refit = mdtCalib_functions.lineConv(line)
    #             rTrk_refit = mdtCalib_functions.dist(locY,locZ,m_refit,b_refit)
    #             residual_new = np.abs(radial)- np.abs(rTrk_refit)
    #             track_chi2_new = sum((np.abs(radial)-np.abs(rTrk_refit))**2/resSigma**2)/(len(radial)-1)
    #             all_chi2.append(track_chi2_new)
    #             all_mbList.append((m_refit,b_refit))

    #             if track_chi2_new < 500. :
    #                 chi2List.append(track_chi2_new)
    #                 lineList.append(list(line))
    #         #print('searching points : %d and %d'%(n-1,n))
    #         #matchedLine,chi2 = mdtCalib_functions.getMatchedLine(lines,seg,resSigma)
    #         #matchedLine,chi2 = mdtCalib_functions.getCandidateLines(lines,seg,resSigma)
    #         if len(chi2List) > 0 :
    #             cand_chi2.append(chi2List)
    #             cand_line.append(lineList)

    #     # pick the exist best chi2 track
    #     best_chi2 = all_chi2[np.argmin(all_chi2)]
    #     best_m_refit,best_b_refit = all_mbList[np.argmin(all_chi2)]

    #     # loop all combinations to do once again
    #     if (len(cand_line)==0) :
    #         print('refit failed because of less 2 hits on track')
    #         return ax,(best_m_refit,best_b_refit), best_chi2
    #     #print(cand_line)
    #     reconLines = list(itertools.product(*cand_line))
    #     #print(len(reconLines),reconLines)
    #     chi2List = []
    #     mbList = []
    #     for line in reconLines :
    #         #print (line)
    #         xline = xSL.xStraightLine(line)
    #         m_refit,b_refit = xline.mb
    #         rTrk_refit,track_chi2_new = xline.dist2line(seg,resSigma)
    #         # rTrk_refit = mdtCalib_functions.dist(locY,locZ,m_refit,b_refit)
    #         # residual_new = np.abs(radial)- np.abs(rTrk_refit)
    #         # track_chi2_new = sum((np.abs(radial)-np.abs(rTrk_refit))**2/resSigma**2)/(len(radial)-1)
    #         chi2List.append(track_chi2_new)
    #         mbList.append((m_refit,b_refit))
    #     #print ('final chi2list :',chi2List)
    #     index = np.argmin(chi2List)
    #     m_chi2 = chi2List[index]
    #     reconPoints = reconLines[index]
    #     m_refit,b_refit = mbList[index]
    #     # reconPoints.append(matchedLine)

    #     x = []
    #     y = []
    #     for point in reconPoints :
    #         x1,y1,x2,y2 = point
    #         x.append(x1)
    #         x.append(x2)
    #         y.append(y1)
    #         y.append(y2)
    #     #print(len(reconPoints),reconPoints)

    #     # check the rTrk and reject flase hits

    #     # refit segment hits to new track line
    #     #ax.plot(x,y,'r.',label='reconPoints')
    #     m_refit,b_refit = np.polyfit(x, y, 1)

    #     # compare m_chi2 and best_chi2
    #     if m_chi2 > best_chi2 :
    #         m_refit,b_refit = best_m_refit,best_b_refit

    #     rTrk_refit = mdtCalib_functions.dist(locY,locZ,m_refit,b_refit)
    #     residual_new = np.abs(radial)- np.abs(rTrk_refit)
    #     track_chi2_new = sum((np.abs(radial)-np.abs(rTrk_refit))**2/resSigma**2)/(len(radial)-1)

    #     # compare default chi2 and refitted_chi2
    #     track_chi2_old = sum((np.abs(radial)-np.abs(rTrk))**2/resSigma**2)/(len(radial)-1)
    #     if track_chi2_new > track_chi2_old :
    #         m_def = float(self.df.seg_dirZ)/float(self.df.seg_dirY)
    #         b_def = float(self.df.seg_posZ) - m_def*float(self.df.seg_posY)
    #         return ax, (m_def,b_def), track_chi2_old

    #     xx = np.linspace(np.min(locY)-20,np.max(locY)+20, 1000)
    #     ax.plot(xx, m_refit*xx + b_refit ,'m--',label='refitted segment with chi2 %.3f'%track_chi2_new)
    #     #ax.plot(xx, best_m_refit*xx + best_b_refit ,'g--',label='best_refitted segment with chi2 %.3f'%best_chi2)

    #     #if info :
    #         #ax.text(np.min(locY)-100,np.max(locZ)+40,'new Residual : %s\nNew chi2 : %.3f'%(residual_new,track_chi2_new), color = 'r')
    #     ax.legend()
    #     return ax,(m_refit,b_refit),track_chi2_new

    #     #return 1, rTrk_refit, track_chi2_new,(m_refit,b_refit)

    # def refitSegment(self, ax, info):

    #     # next implement the hit map
    #     locY = [float(y) for y in self.df.mdt_posY[1:-1].split(', ')]
    #     locZ = [float(y) for y in self.df.mdt_posZ[1:-1].split(', ')]
    #     radial = np.abs([float(y) for y in self.df.mdt_r[1:-1].split(', ')])
    #     #radial = np.abs([float(y) for y in x.newR[1:-1].split(', ')])

    #     # construct seg and hit points
    #     seg = locY,locZ,np.abs(radial)
    #     points = list(zip(locY,locZ,np.abs(radial)))
    #     #print(len(points),points)
    #     reconPoints = []

    #     # create resolution function for chi2 calcualtion
    #     resolution_constants=self.resolution_constants[0]
    #     if self.chamber[:3] in ['BMG','BME']:
    #         resolution_constants=self.resolution_constants[1]

    #     #z=np.array([-0.27691671, 6.43554103, -55.16984486, 240.10554353])
    #     resSigma = np.polyval(resolution_constants,np.abs(radial))/1000.

    #     # loop all hits and get reconPoints
    #     best_chi2 = 100.
    #     cand_chi2 = []
    #     cand_line = []
    #     all_chi2 = []
    #     all_mbList = []
    #     for n in np.arange(1,len(points)) :
    #         lines = mdtCalib_functions.tangentLine(points[n-1],points[n],0)
    #         for line in lines :
    #             # lline = []
    #             # lline.append(line)
    #             # xline = xSL.xStraightLine(line)
    #             # m_refit,b_refit = xline.mb
    #             # rTrk_refit,track_chi2_new = xline.dist2line(seg,resSigma)
    #             m_refit,b_refit = mdtCalib_functions.lineConv(line)
    #             rTrk_refit = mdtCalib_functions.dist(locY,locZ,m_refit,b_refit)
    #             residual_new = np.abs(radial)- np.abs(rTrk_refit)
    #             track_chi2_new = sum((np.abs(radial)-np.abs(rTrk_refit))**2/resSigma**2)/(len(radial)-1)
    #             all_chi2.append(track_chi2_new)
    #             all_mbList.append((m_refit,b_refit))
    #         #print('searching points : %d and %d'%(n-1,n))
    #         #matchedLine,chi2 = mdtCalib_functions.getMatchedLine(lines,seg,resSigma)
    #         matchedLine,chi2 = mdtCalib_functions.getCandidateLines(lines,seg,resSigma)
    #         if len(chi2) > 0 :
    #             cand_chi2.append(chi2)
    #             cand_line.append(matchedLine)

    #     # pick the exist best chi2 track
    #     best_chi2 = all_chi2[np.argmin(all_chi2)]
    #     best_m_refit,best_b_refit = all_mbList[np.argmin(all_chi2)]

    #     # loop all combinations to do once again
    #     if (len(cand_line)<3) :
    #         print('refit failed because of less 3 hits on track')
    #         return ax,(best_m_refit,best_b_refit),best_chi2
    #     #print(cand_line)
    #     reconLines = list(itertools.product(*cand_line))
    #     #print(len(reconLines),reconLines)
    #     chi2List = []
    #     mbList = []
    #     for line in reconLines :
    #         #print (line)
    #         xline = xSL.xStraightLine()
    #         xline.setPoints(reconPoint)
    #         xline.points2line()
    #         m_refit,b_refit = xline.mb
    #         rTrk_refit,track_chi2_new = xline.dist2line(seg,resSigma)
    #         # rTrk_refit = mdtCalib_functions.dist(locY,locZ,m_refit,b_refit)
    #         # residual_new = np.abs(radial)- np.abs(rTrk_refit)
    #         # track_chi2_new = sum((np.abs(radial)-np.abs(rTrk_refit))**2/resSigma**2)/(len(radial)-1)
    #         chi2List.append(track_chi2_new)
    #         mbList.append((m_refit,b_refit))
    #     #print ('final chi2list :',chi2List)
    #     index = np.argmin(chi2List)
    #     m_chi2 = chi2List[index]
    #     reconPoints = reconLines[index]
    #     m_refit,b_refit = mbList[index]
    #     # reconPoints.append(matchedLine)

    #     x = []
    #     y = []
    #     for point in reconPoints :
    #         x1,y1,x2,y2 = point
    #         x.append(x1)
    #         x.append(x2)
    #         y.append(y1)
    #         y.append(y2)
    #     #print(len(reconPoints),reconPoints)

    #     # check the rTrk and reject flase hits

    #     # refit segment hits to new track line
    #     ax.plot(x,y,'r.',label='reconPoints')
    #     m_refit,b_refit = np.polyfit(x, y, 1)
    #     #if m_chi2 > best_chi2 :
    #     #    m_refit,b_refit = best_m_refit,best_b_refit

    #     rTrk_refit = mdtCalib_functions.dist(locY,locZ,m_refit,b_refit)
    #     residual_new = np.abs(radial)- np.abs(rTrk_refit)
    #     track_chi2_new = sum((np.abs(radial)-np.abs(rTrk_refit))**2/resSigma**2)/(len(radial)-1)

    #     xx = np.linspace(np.min(locY)-20,np.max(locY)+20, 1000)
    #     ax.plot(xx, m_refit*xx + b_refit ,'m--',label='%s refitted segment with chi2 %.3f'%(self.df.seg_station, track_chi2_new))
    #     #ax.plot(xx, best_m_refit*xx + best_b_refit ,'g--',label='best_refitted segment with chi2 %.3f'%best_chi2)

    #     #if info :
    #     #    ax.text(np.min(locY)-100,np.max(locZ)+40,'new Residual : %s\nNew chi2 : %.3f'%(residual_new,track_chi2_new), color = 'r')
    #     ax.legend()

    #     return ax,(m_refit,b_refit),track_chi2_new

    # method of calculation unbais residual ( remove one hit from segments and get residual from the track of all rest hits )
    def applyUnbiasResidual(self, q, resolution_constants):
        # next implement the hit map
        locY = [float(y) for y in self.df.mdt_posY[q][1:-1].split(', ')]
        locZ = [float(y) for y in self.df.mdt_posZ[q][1:-1].split(', ')]
        radial = np.abs([float(y) for y in self.df.mdt_r[q][1:-1].split(', ')])
        # radial = np.abs([float(y) for y in x.newR[1:-1].split(', ')])
        resSigma = np.polyval(resolution_constants, np.abs(radial)) / 1000.

        # construct seg and hit points
        seg = locY, locZ, np.abs(radial)
        points = list(zip(locY, locZ, np.abs(radial)))

        unbais_rTrk = []
        # return -99. array if points < 4
        if len(points) < 4:
            unbais_rTrk = [-99. for n in np.arange(len(points))]
            return unbais_rTrk
        # loop each points and get residual of each points
        for j, point in enumerate(points):
            rPoints = points.copy()
            del rPoints[j]
            # print(j,rPoints)

            # tracking the minimum chi2 track
            min_chi2 = 999.
            min_m, min_b = 0., 0.
            approching_points = []
            # initial points array
            for i in np.arange(0, len(rPoints)):
                approching_points.append(([], []))

            for n in np.arange(1, len(rPoints)):
                # skip case x,y of two points are same

                # if points[n-1][0] == points[n][0] and points[n-1][1] == points[n][1]: continue
                # make all 4 tangentLines and return two points coor
                lines = mdtCalib_functions.tangentLine(rPoints[n - 1], rPoints[n], 0)
                for i, line in enumerate(lines):
                    x1, y1, x2, y2 = line
                    # print(i,line)
                    approching_points[n - 1][0].append(x1)
                    approching_points[n - 1][1].append(y1)
                    approching_points[n][0].append(x2)
                    approching_points[n][1].append(y2)

                for line in lines:
                    # load points into approching_points array
                    m, b = mdtCalib_functions.lineConv(line)
                    rTrk_temp = mdtCalib_functions.dist(seg[0], seg[1], m, b)
                    # residual_temp = np.abs(seg[2])- np.abs(rTrk_temp)
                    track_chi2_temp = sum((np.abs(seg[2]) - np.abs(rTrk_temp)) ** 2 / resSigma ** 2) / (len(seg[2]) - 1)

                    if track_chi2_temp < min_chi2:
                        min_m, min_b = m, b
                        min_chi2 = track_chi2_temp

            # print(approching_points)
            # new method to find the approching points of each hit circle
            xxx = []
            yyy = []
            if min_m != 0. and min_b != 0.:
                for m, ap in enumerate(approching_points):
                    # print(m,ap)
                    rTrk_t = mdtCalib_functions.dist(ap[0], ap[1], min_m, min_b)
                    # find the smallest rTrk_t
                    # print(rTrk_t)
                    index = np.argmin(rTrk_t)
                    xxx.append(ap[0][index])
                    yyy.append(ap[1][index])

            # return -99. array if points < 4
            if len(xxx) < 2 or len(yyy) < 2:
                # unbais_rTrk = [-99. for n in np.arange(len(points))]
                # print(xxx,yyy)
                unbais_rTrk.append(-99.)
            else:
                # ax.plot(np.array(xxx), np.array(yyy),'r.',label = 'new_reconPoints')
                m_refit, b_refit = np.polyfit(xxx, yyy, 1)
                new_rTrk_temp = mdtCalib_functions.dist(seg[0], seg[1], m_refit, b_refit)
                # min_track_chi2_refit = sum((np.abs(seg[2])-np.abs(new_rTrk_temp))**2/resSigma**2)/(len(seg[2])-1)
                # ax.plot(xx, m_refit*xx + b_refit,label='%s refitted segment,refit %d with new min chi2 %.3f, rTrk_unbais %.3f'%(test_df.seg_station,j, min_track_chi2_refit,new_rTrk_temp[j]))
                unbais_rTrk.append(new_rTrk_temp[j])

        return unbais_rTrk

    # draw refitSegment
    def drawRefitSegment(self, q, ax, resolution_constants):

        locY = [float(y) for y in self.df.mdt_posY[q][1:-1].split(', ')]
        # locZ = [float(y) for y in self.df.mdt_posZ[1:-1].split(', ')]
        xx = np.linspace(np.min(locY) - 20, np.max(locY) + 20, 1000)
        refitFlag, chi2_refit, chi2_def, rTrk_refit, xline = self.applyRefitSegment(q, resolution_constants)
        m_refit, b_refit = xline.getMB()
        ax.plot(xx, m_refit * xx + b_refit, 'm--', label='%s refitted segment with new chi2 %.3f def chi2 %.3f' % (
        self.df.chamber, chi2_refit, chi2_def))
        ax.legend()
        return ax

    # info flag to display segment info
    def applyRefitSegment(self, q, resolution_constants):
        # next implement the hit map
        #locY = [float(y) for y in self.df.mdt_posY[1:-1].split(', ')]
        locY = [float(y) for y in self.df.mdt_posY[q][1:-1].split(', ')]
        #locZ = [float(y) for y in self.df.mdt_posZ[1:-1].split(', ')]
        locZ = [float(y) for y in self.df.mdt_posZ[q][1:-1].split(', ')]
        #radial = [float(y) for y in self.df.mdt_r[1:-1].split(', ')]
        radial = [float(y) for y in self.df.mdt_r[q][1:-1].split(', ')]
        #rTrk = [float(y) for y in self.df.mdt_rTrk[1:-1].split(', ')]
        rTrk = [float(y) for y in self.df.mdt_rTrk[q][1:-1].split(', ')]
        #tubeIds = [y for y in self.df.mdt_tubeInfo[2:-2].split('\', \'')]
        tubeIds = [y for y in self.df.mdt_chamber[0][2:-2].split('\', \'')]

        # construct seg and hit points
        seg = locY, locZ, radial, rTrk, tubeIds

        resSigma = np.polyval(resolution_constants, np.abs(radial)) / 1000.
        # resSigma = np.polyval(self.resolution_constants,np.abs(radial))/1000.

        # draw default segment direction and chi2
        #float(y) for y in self.df.seg_posY[x][1:-1].split(', ')
        m_def = float(self.df.seg_dirZ[q]) / float(self.df.seg_dirY[q])
        b_def = float(self.df.seg_posZ[q]) - m_def * float(self.df.seg_posY[q])
        #m_def = np.array([float(y) for y in self.df.seg_dirZ[q][1:-1].split(', ')]) / np.array([float(y) for y in self.df.seg_dirY[q][1:-1].split(', ')])
        #b_def = np.array([float(y) for y in self.df.seg_posZ[q][1:-1].split(', ')]) - m_def * np.array([float(y) for y in self.df.seg_posY[q][1:-1].split(', ')])
        # default residual and track_chi2
        chi2_def = sum((np.abs(seg[2]) - np.abs(seg[3])) ** 2 / resSigma ** 2) / (len(seg[2]) - 1)
        # xx = np.linspace(np.min(seg[0])-20,np.max(seg[0])+20, 1000)
        # ax.plot(xx, m_def*xx + b_def ,label='%s default segment calc-chi2 %.3f defChi2 %.3f'%(self.df.seg_station,track_chi2_def,self.df.seg_chi2))

        refitFlag, chi2_refit, rTrk_refit, xline = self.reconStraightLine_minChi2(seg, resSigma)

        # refitFlag, chi2_refit, rTrk_refit, xline = self.reconStraightLine_minChi2(seg,resSigma)

        # if reconStraightLine failed, and refitFlag = 0, return default direction and chi2
        # if refitFlag == 0 or chi2_refit > chi2_def:
        if refitFlag == 0:
            # refitFlag = 0
            chi2_refit = chi2_def
            rTrk_refit = rTrk
            xline = xSL.xStraightLine()
            xline.setMB(m_def, b_def)

        return refitFlag, chi2_refit, chi2_def, rTrk_refit, xline

    def reconStraightLine_minChi2(self, seg, resSigma):
        # set maxRadius
        maxRadius = 14.6
        if seg[4][0][:3] in ['BMG', 'BME']:
            maxRadius = 7.1

        # loop all hits and get reconPoints, make sure radius is positive and clip maxRadius at 7.1
        r = np.clip(np.abs(seg[2]), a_min=0, a_max=maxRadius)
        points = list(zip(seg[0], seg[1], r))
        cand_chi2 = []
        cand_line = []

        # tracking the minimum chi2 track
        min_chi2 = 9990.
        min_m, min_b = 0., 0.
        approching_points = []
        # initial points array
        for i in np.arange(0, len(points)):
            approching_points.append(([], []))

        for n in np.arange(1, len(points)):
            # skip case x,y of two points are same

            # if points[n-1][0] == points[n][0] and points[n-1][1] == points[n][1]: continue
            # make all 4 tangentLines and return two points coor
            lines = mdtCalib_functions.tangentLine(points[n - 1], points[n], 0)

            for line in lines:
                x1, y1, x2, y2 = line
                approching_points[n - 1][0].append(x1)
                approching_points[n - 1][1].append(y1)
                approching_points[n][0].append(x2)
                approching_points[n][1].append(y2)
            # lines = mdtCalib_functions.tangentLine(point[0],point[1],0)
            for line in lines:
                # a,b,c = mdtCalib_functions.twoPoints2line(line)
                # rTrk_temp = mdtCalib_functions.dist_abc(seg[0],seg[1],a,b,c)
                m, b = mdtCalib_functions.lineConv(line)
                rTrk_temp = mdtCalib_functions.dist(seg[0], seg[1], m, b)

                # residual_temp = np.abs(seg[2])- np.abs(rTrk_temp)
                track_chi2_temp = sum((np.abs(seg[2]) - np.abs(rTrk_temp)) ** 2 / resSigma ** 2) / (len(seg[2]) - 1)
                if track_chi2_temp < min_chi2:
                    min_m, min_b = m, b
                    min_chi2 = track_chi2_temp
        if min_chi2 >= 9999:
            return 0, -999., seg[3], xSL.xStraightLine()

        else:
            # new method to find the approching points of each hit circle
            xxx = []
            yyy = []
            if min_m != 0. and min_b != 0.:
                for m, ap in enumerate(approching_points):
                    # print(m,ap)
                    rTrk_t = mdtCalib_functions.dist(ap[0], ap[1], min_m, min_b)
                    # find the smallest rTrk_t
                    # print(rTrk_t)
                    index = np.argmin(rTrk_t)
                    xxx.append(ap[0][index])
                    yyy.append(ap[1][index])

            # print(xxx,yyy)
            # ax.plot(np.array(xxx), np.array(yyy),'b.',label = 'new_reconPoints')
            if len(xxx) < 2 or len(yyy) < 2:
                return 0, -999., seg[3], xSL.xStraightLine()
            m_refit, b_refit = np.polyfit(xxx, yyy, 1)
            new_rTrk_temp = mdtCalib_functions.dist(seg[0], seg[1], m_refit, b_refit)
            min_track_chi2_refit = sum((np.abs(seg[2]) - np.abs(new_rTrk_temp)) ** 2 / resSigma ** 2) / (
                        len(seg[2]) - 1)
            xline = xSL.xStraightLine()
            xline.setMB(m_refit, b_refit)
            # ax.plot(xx, m_refit*xx + b_refit,label='%s refitted segment with new min chi2 %.3f'%(test_df.seg_station, min_track_chi2_refit))
            return 1, min_track_chi2_refit, list(new_rTrk_temp), xline

    def reconStraightLine(self, seg, resSigma):

        # set maxRadius
        maxRadius = 14.6
        if seg[4][0][:3] in ['BMG', 'BME']:
            maxRadius = 7.1

        # loop all hits and get reconPoints, make sure radius is positive and clip maxRadius at 7.1
        r = np.clip(np.abs(seg[2]), a_min=0, a_max=maxRadius)
        points = list(zip(seg[0], seg[1], r))
        cand_chi2 = []
        cand_line = []
        # make all hits combinations
        # pairPoints = itertools.combinations(points, 2)
        # for point in pairPoints:
        #     if point[0][0] == points[1][0] and points[0][1] == points[1][1]: continue
        min_chi2 = 9999
        min_m, min_b = 0., 0.

        for n in np.arange(1, len(points)):
            # skip case x,y of two points are same

            # if points[n-1][0] == points[n][0] and points[n-1][1] == points[n][1]: continue
            # make all 4 tangentLines and return two points coor
            lines = mdtCalib_functions.tangentLine(points[n - 1], points[n], 0)
            # lines = mdtCalib_functions.tangentLine(point[0],point[1],0)

            chi2List = []
            lineList = []
            for line in lines:
                # a,b,c = mdtCalib_functions.twoPoints2line(line)
                # rTrk_temp = mdtCalib_functions.dist_abc(seg[0],seg[1],a,b,c)
                m, b = mdtCalib_functions.lineConv(line)
                rTrk_temp = mdtCalib_functions.dist_mb(seg[0], seg[1], m, b)

                # residual_temp = np.abs(seg[2])- np.abs(rTrk_temp)
                track_chi2_temp = sum((np.abs(seg[2]) - np.abs(rTrk_temp)) ** 2 / resSigma ** 2) / (len(seg[2]) - 1)
                # print(rTrk_temp, residual_temp, track_chi2_temp)
                # if np.sum(residual_temp[np.abs(residual_temp) > roadWidth]) :
                if track_chi2_temp < min_chi2:
                    min_m, min_b = m, b
                    min_chi2 = track_chi2_temp
                if track_chi2_temp > 400:
                    continue
                    # print(line, 'roadWidth bad track')
                else:
                    # print(line, 'roadWidth good track')
                    # print good sub-track
                    # ax.plot([line[0],line[2]],[line[1],line[3]],label='roadwidth_candidate %d, chi2 %.3f'%(n,track_chi2_temp))
                    chi2List.append(track_chi2_temp)
                    lineList.append(line)
                    # fill the list of all segment candidates
            if len(chi2List) > 0:
                cand_chi2.append(chi2List)
                cand_line.append(lineList)

                # loop over the combinations of all sub-segments once again
        if (len(cand_line) < 1):
            # print('refit failed because of less 3 hits on reconstruction track')
            return 0, -999., seg[3], xSL.xStraightLine(), -999.
        else:
            # create all combinations of sub-segment tracks
            reconPoints = list(itertools.product(*cand_line))
            # print(len(reconPoints),reconPoints)
            cand_chi2List = []
            cand_xlineList = []
            cand_rTrkList = []

            for reconPoint in reconPoints:
                xline = xSL.xStraightLine()
                xline.setPoints(reconPoint)
                xline.points2line()
                m_refit, b_refit = xline.mb
                track_chi2_refit, rTrk_refit = xline.dist2line_mb(seg, resSigma)
                # xx = np.linspace(np.min(seg[0])-20,np.max(seg[0])+20, 1000)
                # ax.plot(xx, m_refit*xx + b_refit,label='%s refitted segment with chi2 %.3f'%(self.df.seg_station, track_chi2_refit))
                # rTrk_refit = mdtCalib_functions.dist(locY,locZ,m_refit,b_refit)
                # residual_new = np.abs(radial)- np.abs(rTrk_refit)
                # track_chi2_new = sum((np.abs(radial)-np.abs(rTrk_refit))**2/resSigma**2)/(len(radial)-1)
                cand_chi2List.append(track_chi2_refit)
                cand_xlineList.append(xline)
                cand_rTrkList.append(rTrk_refit)

            # pick up the minimum chi2 final track
            index = np.argmin(cand_chi2List)
            refit_chi2 = cand_chi2List[index]
            refit_rTrk = cand_rTrkList[index]
            refit_line = cand_xlineList[index]
            # print(refit_chi2,refit_line)

            return 1, refit_chi2, refit_rTrk, refit_line, min_chi2

        # points = list(zip(*seg))
        # #print(len(points),points)
        # reconPoints = []

        # # create resolution function for chi2 calcualtion
        # #resolution_constants=np.array([-0.27691671, 6.43554103, -55.16984486, 240.10554353])
        # #z=np.array([-0.27691671, 6.43554103, -55.16984486, 240.10554353])
        # resSigma = np.polyval(resolution_constants,np.abs(radial))/1000.

        # # loop all hits and get reconPoints
        # best_chi2 = 100.
        # cand_chi2 = []
        # cand_line = []
        # all_chi2 = []
        # all_mbList = []
        # for n in np.arange(1,len(points)) :
        #     lines = mdtCalib_functions.tangentLine(points[n-1],points[n],0)
        #     chi2List = []
        #     lineList = []
        #     for line in lines :
        #         # lline = []
        #         # lline.append(line)
        #         # xline = xSL.xStraightLine(line)
        #         # m_refit,b_refit = xline.mb
        #         # rTrk_refit,track_chi2_new = xline.dist2line(seg,resSigma)
        #         m_refit,b_refit = mdtCalib_functions.lineConv(line)
        #         rTrk_refit = mdtCalib_functions.dist(locY,locZ,m_refit,b_refit)
        #         residual_new = np.abs(radial)- np.abs(rTrk_refit)
        #         track_chi2_new = sum((np.abs(radial)-np.abs(rTrk_refit))**2/resSigma**2)/(len(radial)-1)
        #         all_chi2.append(track_chi2_new)
        #         all_mbList.append((m_refit,b_refit))

        #         if track_chi2_new < 500. :
        #             chi2List.append(track_chi2_new)
        #             lineList.append(list(line))
        #     #print('searching points : %d and %d'%(n-1,n))
        #     #matchedLine,chi2 = mdtCalib_functions.getMatchedLine(lines,seg,resSigma)
        #     #matchedLine,chi2 = mdtCalib_functions.getCandidateLines(lines,seg,resSigma)
        #     if len(chi2List) > 0 :
        #         cand_chi2.append(chi2List)
        #         cand_line.append(lineList)

        # # pick the exist best chi2 track
        # best_chi2 = all_chi2[np.argmin(all_chi2)]
        # best_m_refit,best_b_refit = all_mbList[np.argmin(all_chi2)]

        # # loop all combinations to do once again
        # if (len(cand_line)==0) :
        #     print('refit failed because of less 2 hits on track')
        #     return 0,rTrk_refit,best_chi2,(best_m_refit,best_b_refit)
        # #print(cand_line)
        # reconLines = list(itertools.product(*cand_line))
        # #print(len(reconLines),reconLines)
        # chi2List = []
        # mbList = []
        # for line in reconLines :
        #     #print (line)
        #     xline = xSL.xStraightLine(line)
        #     m_refit,b_refit = xline.mb
        #     rTrk_refit,track_chi2_new = xline.dist2line(seg,resSigma)
        #     # rTrk_refit = mdtCalib_functions.dist(locY,locZ,m_refit,b_refit)
        #     # residual_new = np.abs(radial)- np.abs(rTrk_refit)
        #     # track_chi2_new = sum((np.abs(radial)-np.abs(rTrk_refit))**2/resSigma**2)/(len(radial)-1)
        #     chi2List.append(track_chi2_new)
        #     mbList.append((m_refit,b_refit))
        # #print ('final chi2list :',chi2List)
        # index = np.argmin(chi2List)
        # m_chi2 = chi2List[index]
        # reconPoints = reconLines[index]
        # m_refit,b_refit = mbList[index]
        # # reconPoints.append(matchedLine)

        # x = []
        # y = []
        # for point in reconPoints :
        #     x1,y1,x2,y2 = point
        #     x.append(x1)
        #     x.append(x2)
        #     y.append(y1)
        #     y.append(y2)
        # #print(len(reconPoints),reconPoints)

        # # check the rTrk and reject flase hits

        # # refit segment hits to new track line
        # #ax.plot(x,y,'r.',label='reconPoints')
        # m_refit,b_refit = np.polyfit(x, y, 1)

        # # compare m_chi2 and best_chi2
        # #if m_chi2 > best_chi2 :
        # #    m_refit,b_refit = best_m_refit,best_b_refit

        # rTrk_refit = mdtCalib_functions.dist(locY,locZ,m_refit,b_refit)
        # residual_new = np.abs(radial)- np.abs(rTrk_refit)
        # track_chi2_new = sum((np.abs(radial)-np.abs(rTrk_refit))**2/resSigma**2)/(len(radial)-1)

        # # compare default chi2 and refitted_chi2
        # track_chi2_old = sum((np.abs(radial)-np.abs(rTrk))**2/resSigma**2)/(len(radial)-1)
        # if track_chi2_new > track_chi2_old :
        #     m_def = float(self.df.seg_dirZ)/float(self.df.seg_dirY)
        #     b_def = float(self.df.seg_posZ) - m_def*float(self.df.seg_posY)
        #     return 1, rTrk , track_chi2_old, (m_def,b_def)

        # #xx = np.linspace(np.min(locY)-20,np.max(locY)+20, 1000)
        # #ax.plot(xx, m_refit*xx + b_refit ,'m--',label='refitted segment with chi2 %.3f'%track_chi2_new)
        # #ax.plot(xx, best_m_refit*xx + best_b_refit ,'g--',label='best_refitted segment with chi2 %.3f'%best_chi2)

        # #if info :
        # #    ax.text(np.min(locY)-100,np.max(locZ)+40,'new Residual : %s\nNew chi2 : %.3f'%(residual_new,track_chi2_new), color = 'r')
        # #ax.legend()

        # return 1, rTrk_refit, track_chi2_new,(m_refit,b_refit)

    def display(self, ax, info):
        # initial plt,axes
        # fig,ax = plt.subplots(figsize=(20,15))
        # plt.axis('equal')
        # for i in np.arange(len(locX)):
        locX = [float(y) for y in self.df.mdt_posX[1:-1].split(', ')]
        locY = [float(y) for y in self.df.mdt_posY[1:-1].split(', ')]
        locZ = [float(y) for y in self.df.mdt_posZ[1:-1].split(', ')]
        radial = np.abs([float(y) for y in self.df.mdt_r[1:-1].split(', ')])
        rTrk = [float(y) for y in self.df.mdt_rTrk[1:-1].split(', ')]
        patches = []
        tubeIds = [y[8:] for y in self.df.mdt_tubeInfo[2:-2].split('\', \'')]

        tubeRadial = 15
        tubeRadial_wall = 15
        tubeRadial_inner = 14.6
        vshift = 60
        if self.chamber[:3] in ['BMG', 'BME']:
            tubeRadial_wall = 7.5
            tubeRadial_inner = 7.1
            vshift = 30

        # draw hits and tube wall and tubeIds
        for x1, y1, r, rtr, tubeId in zip(locY, locZ, radial, np.abs(rTrk), tubeIds):
            # print(x1,y1,r)
            ax.plot(x1, y1, 'b.')
            circle = Circle((x1, y1), r)
            circle_rtrk = Circle((x1, y1), rtr, fill=False, color='r')
            tube_wall = Circle((x1, y1), tubeRadial_wall, fill=False)
            tube_inner = Circle((x1, y1), tubeRadial_inner, fill=False)
            ax.add_patch(circle)
            ax.add_patch(circle_rtrk)
            ax.add_patch(tube_inner)
            ax.add_patch(tube_wall)
            ax.text(x1 + vshift, y1 + 8, tubeId, fontsize=10, verticalalignment='top', color='b', wrap=True)
            ax.text(x1 + vshift, y1 + 4, 'r=%.2f' % r, fontsize=10, verticalalignment='top', color='b', wrap=True)
            ax.text(x1 + vshift, y1, 'd=%.2f' % rtr, fontsize=10, verticalalignment='top', color='b', wrap=True)

            # patches.append(circle)
        # ax.set_xlim(np.min(locY)-50,np.max(locY)+50)
        # ax.set_ylim(np.min(locZ)-50,np.max(locZ)+50)
        ax.set_ylim(0, 350)
        ax.set_xlabel('LocY [mm]')
        ax.set_ylabel('LocZ [mm]')

        # draw default segment track
        m_def = float(self.df.seg_dirZ) / float(self.df.seg_dirY)
        b_def = float(self.df.seg_posZ) - m_def * float(self.df.seg_posY)
        # print(m_def,b_def)
        # draw segment default direction
        # def segLine(x):
        #    return m_def*x+b_def
        # ax4.plot(xx, segLine(xx),'b--',label='default segment')
        # default residual and track_chi2
        # resolution_constants=np.array([-0.27691671, 6.43554103, -55.16984486, 240.10554353])
        resSigma = np.polyval(self.resolution_constants, np.abs(radial)) / 1000.
        residual_old = np.abs(radial) - np.abs(rTrk)
        track_chi2_old = sum((np.abs(radial) - np.abs(rTrk)) ** 2 / resSigma ** 2) / (len(radial) - 1)
        xx = np.linspace(np.min(locY) - 20, np.max(locY) + 20, 1000)
        ax.plot(xx, m_def * xx + b_def, 'b--', label='%s default segment chi2 %.3f defChi2 %.3f' % (
        self.df.seg_station, track_chi2_old, self.df.seg_chi2))
        # if info :
        # ax.text(np.min(locY)-100, np.max(locZ)+20, 'old residual : %s \nold chi2 : %s '%(residual_old,track_chi2_old),fontsize=10, verticalalignment='top',color='b',wrap=True)

        # ax4.text(np.min(locY)-100,np.max(locZ),'Old chi2 : %.3f\nNew chi2 : %.3f\nBest chi2 : %.3f'%(track_chi2_old,track_chi2_new,track_chi2_best),color = 'r')
        # textstr = self.df.mdt_tubeInfo
        # ax.text(np.min(locY)-100, np.max(locZ)+30, 'TubeIds : %s'%textstr, fontsize=10, verticalalignment='top',color='b',wrap=True)
        # textstr2 = self.df.mdt_posX
        # ax.text(np.min(locY), np.max(locZ)+40, '2nd Coordinators : %s'%textstr2, fontsize=10, verticalalignment='top',color='b',wrap=True)
        ax.legend()

        return ax

        # call mdtCalib_functions