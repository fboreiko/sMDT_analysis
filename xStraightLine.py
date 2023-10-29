import numpy as np
import mdtCalib_functions


# v2 2705/2020
# two way to initial xStraightLine class
# xline = xSL.xStraightLine()
# 1) xline.setPoints(points)
#    xline.points2line()
# 2) xline.setMB(m,b)
# m,b = xline.mb

# v3 03/06/2020
# move line defination from y = m*x + b to ax+by+c =0
# change the object init
# change the function for calculating the trqck distacne

class xStraightLine:
    def __init__(self):
        # initial line with abc a*x + b*y + c = 0
        # initial line with slope m = 0 and intercept b = 0
        self.abc = 0.0, 0.0, 0.0
        self.mb = 0.0, 0.0
        self.points = []
        # self.rTrk, self.chi2 = self.dist2line()

    def setPoints(self, points):
        self.points = points

    def setMB(self, m, b):
        self.mb = m, b

    def getPoints(self):
        return self.points

    def getMB(self):
        return self.mb

    # function to convert two points (x1,y1),(x2,y2) to a,b,c
    def twoPoints2line(self):
        if len(self.points) == 2:
            x1, y1, x2, y2 = self.points
            a = y2 - y1
            b = x1 - x2
            c = a * x1 + b * y1
            self.abc = a, b, c
        else:
            return 0
        return 1

    # new function to convert line (x1,y1),(x2,y2) to m,b by curved_fit with error
    def points2line(self):
        if len(self.points) > 0:
            x = []
            y = []
            for point in self.points:
                x1, y1, x2, y2 = point
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)

            m_refit, b_refit = np.polyfit(x, y, 1)
            self.mb = m_refit, b_refit
            return 1
        else:
            self.mb = 0.0, 0.0
            return 0

    # function to convert line (x1,y1),(x2,y2) to m,b
    def points2line(self):
        if len(self.points) > 0:
            x = []
            y = []
            for point in self.points:
                x1, y1, x2, y2 = point
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)
            m_refit, b_refit = np.polyfit(x, y, 1)
            self.mb = m_refit, b_refit
            return 1
        else:
            self.mb = 0.0, 0.0
            return 0

    # calcualte rTrk by line.abd and tube hits
    def dist2line_abc(self, seg, resSigma):
        locY, locZ, radial, _, _ = seg
        a, b, c = self.abc
        rTrk_refit = np.abs(a * locY + b * locZ + c) / (np.sqrt(a * a + b * b))
        # rTrk_refit = mdtCalib_functions.dist(locY,locZ,m_refit,b_refit)
        # residual = np.abs(radial)- np.abs(rTrk_refit)
        chi2 = sum((np.abs(radial) - np.abs(rTrk_refit)) ** 2 / resSigma ** 2) / (len(radial) - 1)
        return chi2, rTrk_refit

    # calcualte rTrk by line.mb and tube hits
    def dist2line_mb(self, seg, resSigma):
        locY, locZ, radial, rTrk, tubeIds = seg
        m_refit, b_refit = self.mb
        rTrk_refit = mdtCalib_functions.dist_mb(locY, locZ, m_refit, b_refit)
        # residual = np.abs(radial)- np.abs(rTrk_refit)
        chi2 = sum((np.abs(radial) - np.abs(rTrk_refit)) ** 2 / resSigma ** 2) / (len(radial) - 1)
        return chi2, rTrk_refit

# class xStraightLine :
#     def __init__(self, points) :
#         self.points = points
#         self.mb = self.points2line()
#         #self.rTrk, self.chi2 = self.dist2line()

#     # function to convert line (x1,y1),(x2,y2) to m,b
#     def points2line(self):
#         x = []
#         y = []
#         for point in self.points :
#             x1,y1,x2,y2 = point
#             x.append(x1)
#             x.append(x2)
#             y.append(y1)
#             y.append(y2)
#         m_refit,b_refit = np.polyfit(x, y, 1)
#         return m_refit,b_refit

#     def dist2line(self, seg, resSigma) :
#         locY,locZ,radial,rTrk, tubeIds = seg
#         m_refit,b_refit = self.mb
#         rTrk_refit = mdtCalib_functions.dist(locY,locZ,m_refit,b_refit)
#         #residual = np.abs(radial)- np.abs(rTrk_refit)
#         chi2 = sum((np.abs(radial)-np.abs(rTrk_refit))**2/resSigma**2)/(len(radial)-1)
#         return rTrk_refit,chi2