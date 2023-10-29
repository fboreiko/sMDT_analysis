#! /usr/bin/env python
# A structure listing all chamber names and their geometry parameters
# many routines to access them and to have an easy mapping
#
#  Use like this:
# import chamberlist
# idx=chamberlist.MDTindex("BIL1A01")
#
#  List of methods.  Generally these return -1 to indicate failure
#  CheckChamber( chamber, ml, layer, tube )   => Check for valid
#                   chamber name. Returns mdt[] index of chamber
#  MDTindex( ChName/muonfixedid ) => Returns index in mdt[] for ChName or muonfixedid
#  MDTmfid( ChName, ml=1, ly=1, tb=1 ) => Returns muonfixedid for ChName.
#    or MDTmfid( ChName, mllt ) => Returns muonfixedid for ChName.
#  MDTcheckMfid( mfid )     => Returns MDTindex if mfid is valid; -1 if not
#  MDThardname( idx )       => Returns hardware/online name from idx
#              (idx can be mdt[] index, calname, or muonfixedid)
#  MDTcalname( idx )       => Returns calname/offline name from idx
#              (idx can be mdt[] index, hardname, or muonfixedid)
#  MDTtubename( muonfixedid ) => Returns hardware name-ML-L-T from a muonfixedid
#  MDTnML(  ChName )        => Returns number of ML in the chamber
#  MDTtotalLayers( ChName ) => Returns number of Layers in the chamber
#  MDTtotalTubes( ChName )  => Returns TOT number of Tubes  in the chamber
#  MDTnmezz( ChName )       => Returns number of Mezzanines in the chamber
#  MDTmaxmezz( ChName )     => Returns number of mezzcards included skipped mezzcards due to cut outs
#  MDTtypeML( ChName, ml )  => Returns the ML MEZZ type (1-4)
#  MDTtypeMZ( ChName, mz )  => Returns the MZ MEZZ type (1-4)
#  MDTmlMZ0( ChName )       => Returns ML number where there is Mezz number 0
#  MDTmlMZ( ChName, mz )    => Returns ML number of Mezz number mz
#  MDTnLml( ChName, ml )    => Returns number of Layers in the ML ml=0=both ML
#  MDTnTly( ChName, ml )    => Returns number of Tubes/Layer in the ML  ml=0=both ML
#  MDTnTml( ChName, ml )    => Returns number of Tubes in the ML
#  MLLT2MLLT( ChName, mllt) => Convert MLLT to ml, ly, tb; Returns tuple ml, ly, tb
#                              MLLT = 1000*ml + 100*ly + tb
#  T2MLLT( ChName, tb )     => tubeNumber to MLLT  tubeNumber=[1..<total tubes>]
#  MLLT2T( ChName, mllt )   => MLLT to tubeNumber  [1..<total tubes>]
#  MLLT2L( ChName, mllt )   => MLLT to layerNumber [1..<total layers>]
#  MLLT2M( ChName, mllt )   => MLLT to mezzNumber  [0.. ]
#  MLLT2M( ChName, mllt )   => tubeNumber to mezzNumber
#  MLLT2MezzCh( cham,mllt ) => From cham,mllt return tuple of mezzcard type, mezzcard channel
#  getdate(date)            => Convert date from DD-<Month>-YYYY to YYYYMMDD
#  new function 20180516
#  MDTtubeIndex(ChName, ml,ly,tube )    => Calculate the tube Index by ml,ly,tube
#  MDTtubeIndex2MLLT(ChName, tubeIndex )    => Calculate the MLLT by tubeIndex
#  MDTasdIndex(muonfixedid)    => Calculate the ASD index by muonfixedid, #ASD = idx*1000+#Mezz*10+#ASD (1,2,3)
#
#  Number of mezzcards per ML
#  ntl_ml1(2)/24/nly_ml1(2) or ntl_ml1(2)/(mzt_ml1(2)<3?8:6)
import sys, muonfixedid


class ChInfo:
    "Info for a single MDT chamber"

    # init class
    def __init__(self, calname, hardname, eta, phi, station, num_ml, nly_ml1, ntl_ml1, nly_ml2, ntl_ml2, n_mezz, mz0ml,
                 mzt_ml1, mzt_ml2, installed):
        self.calname = calname  # software/offline name e.g. BIL_1_1
        self.hardname = hardname  # hardware/online name e.g. BIL1A01
        self.eta = eta  # chamber eta; +=>A, -=>C
        self.phi = phi  # phi [1..8]
        self.station = station  # 3-letter station name, e.g. BIL
        self.num_ml = num_ml  # number of ML
        self.nly_ml1 = nly_ml1  # number of layers in ML1
        self.ntl_ml1 = ntl_ml1  # number of tubes/layer in ML1
        self.nly_ml2 = nly_ml2  # number of layers in ML2
        self.ntl_ml2 = ntl_ml2  # number of tubes/layer in ML2
        self.n_mezz = n_mezz  # number of mezz cards (actual mezzcards, does not include non-existant mezzcards in cutouts)
        self.mz0ml = mz0ml  # number of ML with mezzcard 0 (mezzcards numbered by CSM channel)
        self.mzt_ml1 = mzt_ml1  # ML1 mezzcard type (1 and 2 are 3x8, 3 and 4 4x6)
        self.mzt_ml2 = mzt_ml2  # ML2 mezzcard type
        self.installed = installed  # flag if chamber is currently operational


###  List of all chambers and geometry parameters
mdt = [
    ChInfo("BEE_1_1", "BEE1A02", 1, 1, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 0
    ChInfo("BEE_2_1", "BEE1A04", 1, 2, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 1
    ChInfo("BEE_3_1", "BEE1A06", 1, 3, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 2
    ChInfo("BEE_4_1", "BEE1A08", 1, 4, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 3
    ChInfo("BEE_5_1", "BEE1A10", 1, 5, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 4
    ChInfo("BEE_6_1", "BEE1A12", 1, 6, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 5
    ChInfo("BEE_7_1", "BEE1A14", 1, 7, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 6
    ChInfo("BEE_8_1", "BEE1A16", 1, 8, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 7
    ChInfo("BEE_1_-1", "BEE1C02", -1, 1, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 8
    ChInfo("BEE_2_-1", "BEE1C04", -1, 2, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 9
    ChInfo("BEE_3_-1", "BEE1C06", -1, 3, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 10
    ChInfo("BEE_4_-1", "BEE1C08", -1, 4, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 11
    ChInfo("BEE_5_-1", "BEE1C10", -1, 5, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 12
    ChInfo("BEE_6_-1", "BEE1C12", -1, 6, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 13
    ChInfo("BEE_7_-1", "BEE1C14", -1, 7, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 14
    ChInfo("BEE_8_-1", "BEE1C16", -1, 8, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 15
    ChInfo("BEE_1_2", "BEE2A02", 2, 1, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 16
    ChInfo("BEE_2_2", "BEE2A04", 2, 2, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 17
    ChInfo("BEE_3_2", "BEE2A06", 2, 3, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 18
    ChInfo("BEE_4_2", "BEE2A08", 2, 4, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 19
    ChInfo("BEE_5_2", "BEE2A10", 2, 5, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 20
    ChInfo("BEE_6_2", "BEE2A12", 2, 6, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 21
    ChInfo("BEE_7_2", "BEE2A14", 2, 7, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 22
    ChInfo("BEE_8_2", "BEE2A16", 2, 8, "BEE", 1, 4, 48, 0, 0, 8, 1, 3, 0, 1),  # 23
    ChInfo("BEE_1_-2", "BEE2C02", -2, 1, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 24
    ChInfo("BEE_2_-2", "BEE2C04", -2, 2, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 25
    ChInfo("BEE_3_-2", "BEE2C06", -2, 3, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 26
    ChInfo("BEE_4_-2", "BEE2C08", -2, 4, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 27
    ChInfo("BEE_5_-2", "BEE2C10", -2, 5, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 28
    ChInfo("BEE_6_-2", "BEE2C12", -2, 6, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 29
    ChInfo("BEE_7_-2", "BEE2C14", -2, 7, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 30
    ChInfo("BEE_8_-2", "BEE2C16", -2, 8, "BEE", 1, 4, 48, 0, 0, 8, 1, 4, 0, 1),  # 31
    ChInfo("BIL_1_1", "BIL1A01", 1, 1, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 32
    ChInfo("BIL_2_1", "BIL1A03", 1, 2, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 33
    ChInfo("BIL_3_1", "BIL1A05", 1, 3, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 34
    ChInfo("BIL_4_1", "BIL1A07", 1, 4, "BIL", 2, 4, 24, 4, 24, 8, 1, 4, 3, 1),  # 35
    ChInfo("BIL_5_1", "BIL1A09", 1, 5, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 36
    ChInfo("BIL_7_1", "BIL1A13", 1, 7, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 37
    ChInfo("BIL_1_-1", "BIL1C01", -1, 1, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 38
    ChInfo("BIL_2_-1", "BIL1C03", -1, 2, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 39
    ChInfo("BIL_3_-1", "BIL1C05", -1, 3, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 40
    ChInfo("BIL_4_-1", "BIL1C07", -1, 4, "BIL", 2, 4, 24, 4, 24, 8, 2, 3, 4, 1),  # 41
    ChInfo("BIL_5_-1", "BIL1C09", -1, 5, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 42
    ChInfo("BIL_7_-1", "BIL1C13", -1, 7, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 43
    ChInfo("BIL_1_2", "BIL2A01", 2, 1, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 44
    ChInfo("BIL_2_2", "BIL2A03", 2, 2, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 45
    ChInfo("BIL_3_2", "BIL2A05", 2, 3, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 46
    ChInfo("BIL_4_2", "BIL2A07", 2, 4, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 47
    ChInfo("BIL_5_2", "BIL2A09", 2, 5, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 48
    ChInfo("BIL_7_2", "BIL2A13", 2, 7, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 49
    ChInfo("BIL_1_-2", "BIL2C01", -2, 1, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 50
    ChInfo("BIL_2_-2", "BIL2C03", -2, 2, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 51
    ChInfo("BIL_3_-2", "BIL2C05", -2, 3, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 52
    ChInfo("BIL_4_-2", "BIL2C07", -2, 4, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 53
    ChInfo("BIL_5_-2", "BIL2C09", -2, 5, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 54
    ChInfo("BIL_7_-2", "BIL2C13", -2, 7, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 55
    ChInfo("BIL_1_3", "BIL3A01", 3, 1, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 56
    ChInfo("BIL_2_3", "BIL3A03", 3, 2, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 57
    ChInfo("BIL_3_3", "BIL3A05", 3, 3, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 58
    ChInfo("BIL_4_3", "BIL3A07", 3, 4, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 59
    ChInfo("BIL_5_3", "BIL3A09", 3, 5, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 60
    ChInfo("BIL_7_3", "BIL3A13", 3, 7, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 61
    ChInfo("BIL_1_-3", "BIL3C01", -3, 1, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 62
    ChInfo("BIL_2_-3", "BIL3C03", -3, 2, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 63
    ChInfo("BIL_3_-3", "BIL3C05", -3, 3, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 64
    ChInfo("BIL_4_-3", "BIL3C07", -3, 4, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 65
    ChInfo("BIL_5_-3", "BIL3C09", -3, 5, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 66
    ChInfo("BIL_7_-3", "BIL3C13", -3, 7, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 67
    ChInfo("BIL_1_4", "BIL4A01", 4, 1, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 68
    ChInfo("BIL_2_4", "BIL4A03", 4, 2, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 69
    ChInfo("BIL_3_4", "BIL4A05", 4, 3, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 70
    ChInfo("BIL_4_4", "BIL4A07", 4, 4, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 71
    ChInfo("BIL_5_4", "BIL4A09", 4, 5, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 72
    ChInfo("BIL_7_4", "BIL4A13", 4, 7, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 73
    ChInfo("BIL_1_-4", "BIL4C01", -4, 1, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 74
    ChInfo("BIL_2_-4", "BIL4C03", -4, 2, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 75
    ChInfo("BIL_3_-4", "BIL4C05", -4, 3, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 76
    ChInfo("BIL_4_-4", "BIL4C07", -4, 4, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 77
    ChInfo("BIL_5_-4", "BIL4C09", -4, 5, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 78
    ChInfo("BIL_7_-4", "BIL4C13", -4, 7, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 79
    ChInfo("BIL_1_5", "BIL5A01", 5, 1, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 80
    ChInfo("BIL_2_5", "BIL5A03", 5, 2, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 81
    ChInfo("BIL_3_5", "BIL5A05", 5, 3, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 82
    ChInfo("BIL_4_5", "BIL5A07", 5, 4, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 83
    ChInfo("BIL_5_5", "BIL5A09", 5, 5, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 84
    ChInfo("BIL_7_5", "BIL5A13", 5, 7, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 85
    ChInfo("BIL_1_-5", "BIL5C01", -5, 1, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 86
    ChInfo("BIL_2_-5", "BIL5C03", -5, 2, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 87
    ChInfo("BIL_3_-5", "BIL5C05", -5, 3, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 88
    ChInfo("BIL_4_-5", "BIL5C07", -5, 4, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 89
    ChInfo("BIL_5_-5", "BIL5C09", -5, 5, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 90
    ChInfo("BIL_7_-5", "BIL5C13", -5, 7, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 91
    ChInfo("BIL_1_6", "BIL6A01", 6, 1, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 92
    ChInfo("BIL_2_6", "BIL6A03", 6, 2, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 93
    ChInfo("BIL_3_6", "BIL6A05", 6, 3, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 94
    ChInfo("BIL_4_6", "BIL6A07", 6, 4, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 95
    ChInfo("BIL_5_6", "BIL6A09", 6, 5, "BIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 96
    ChInfo("BIL_7_6", "BIL6A13", 6, 7, "BIL", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 97
    ChInfo("BIL_1_-6", "BIL6C01", -6, 1, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 98
    ChInfo("BIL_2_-6", "BIL6C03", -6, 2, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 99
    ChInfo("BIL_3_-6", "BIL6C05", -6, 3, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 100
    ChInfo("BIL_4_-6", "BIL6C07", -6, 4, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 101
    ChInfo("BIL_5_-6", "BIL6C09", -6, 5, "BIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 102
    ChInfo("BIL_7_-6", "BIL6C13", -6, 7, "BIL", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 103
    ChInfo("BIM_6_1", "BIM1A11", 1, 6, "BIM", 2, 4, 36, 4, 36, 12, 1, 3, 4, 1),  # 104
    ChInfo("BIM_8_1", "BIM1A15", 1, 8, "BIM", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 105
    ChInfo("BIM_6_-1", "BIM1C11", -1, 6, "BIM", 2, 4, 36, 4, 36, 12, 2, 4, 3, 1),  # 106
    ChInfo("BIM_8_-1", "BIM1C15", -1, 8, "BIM", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 107
    ChInfo("BIM_6_2", "BIM2A11", 2, 6, "BIM", 2, 4, 36, 4, 36, 12, 1, 3, 4, 1),  # 108
    ChInfo("BIM_8_2", "BIM2A15", 2, 8, "BIM", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 109
    ChInfo("BIM_6_-2", "BIM2C11", -2, 6, "BIM", 2, 4, 36, 4, 36, 12, 2, 4, 3, 1),  # 110
    ChInfo("BIM_8_-2", "BIM2C15", -2, 8, "BIM", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 111
    ChInfo("BIM_6_3", "BIM3A11", 3, 6, "BIM", 2, 4, 36, 4, 36, 12, 1, 3, 4, 1),  # 112
    ChInfo("BIM_8_3", "BIM3A15", 3, 8, "BIM", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 113
    ChInfo("BIM_6_-3", "BIM3C11", -3, 6, "BIM", 2, 4, 36, 4, 36, 12, 2, 4, 3, 1),  # 114
    ChInfo("BIM_8_-3", "BIM3C15", -3, 8, "BIM", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 115
    ChInfo("BIM_6_4", "BIM4A11", 4, 6, "BIM", 2, 4, 36, 4, 36, 12, 1, 3, 4, 1),  # 116
    ChInfo("BIM_8_4", "BIM4A15", 4, 8, "BIM", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 117
    ChInfo("BIM_6_-4", "BIM4C11", -4, 6, "BIM", 2, 4, 36, 4, 36, 12, 2, 4, 3, 1),  # 118
    ChInfo("BIM_8_-4", "BIM4C15", -4, 8, "BIM", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 119
    ChInfo("BIM_6_5", "BIM5A11", 5, 6, "BIM", 2, 4, 36, 4, 36, 12, 1, 3, 4, 1),  # 120
    ChInfo("BIM_8_5", "BIM5A15", 5, 8, "BIM", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 121
    ChInfo("BIM_6_-5", "BIM5C11", -5, 6, "BIM", 2, 4, 36, 4, 36, 12, 2, 4, 3, 1),  # 122
    ChInfo("BIM_8_-5", "BIM5C15", -5, 8, "BIM", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 123
    ChInfo("BIR_6_1", "BIR1A11", 1, 6, "BIR", 2, 4, 24, 4, 30, 9, 1, 3, 4, 1),  # 124
    ChInfo("BIR_8_1", "BIR1A15", 1, 8, "BIR", 2, 4, 24, 4, 30, 9, 1, 4, 3, 1),  # 125
    ChInfo("BIR_6_-1", "BIR1C11", -1, 6, "BIR", 2, 4, 24, 4, 30, 9, 2, 4, 3, 1),  # 126
    ChInfo("BIR_8_-1", "BIR1C15", -1, 8, "BIR", 2, 4, 24, 4, 30, 9, 2, 3, 4, 1),  # 127
    ChInfo("BIR_6_2", "BIR2A11", 2, 6, "BIR", 2, 4, 27, 4, 30, 10, 1, 3, 4, 1),  # 128
    ChInfo("BIR_8_2", "BIR2A15", 2, 8, "BIR", 2, 4, 27, 4, 30, 10, 1, 4, 3, 1),  # 129
    ChInfo("BIR_6_-2", "BIR2C11", -2, 6, "BIR", 2, 4, 27, 4, 30, 10, 2, 4, 3, 1),  # 130
    ChInfo("BIR_8_-2", "BIR2C15", -2, 8, "BIR", 2, 4, 27, 4, 30, 10, 2, 3, 4, 1),  # 131
    ChInfo("BIR_6_3", "BIR3A11", 3, 6, "BIR", 2, 4, 33, 4, 33, 12, 1, 3, 4, 1),  # 132
    ChInfo("BIR_8_3", "BIR3A15", 3, 8, "BIR", 2, 4, 33, 4, 33, 12, 1, 4, 3, 1),  # 133
    ChInfo("BIR_6_-3", "BIR3C11", -3, 6, "BIR", 2, 4, 33, 4, 33, 12, 2, 4, 3, 1),  # 134
    ChInfo("BIR_8_-3", "BIR3C15", -3, 8, "BIR", 2, 4, 33, 4, 33, 12, 2, 3, 4, 1),  # 135
    ChInfo("BIR_6_4", "BIR4A11", 4, 6, "BIR", 2, 4, 27, 4, 30, 10, 1, 3, 4, 1),  # 136
    ChInfo("BIR_8_4", "BIR4A15", 4, 8, "BIR", 2, 4, 27, 4, 30, 10, 1, 4, 3, 1),  # 137
    ChInfo("BIR_6_-4", "BIR4C11", -4, 6, "BIR", 2, 4, 27, 4, 30, 10, 2, 4, 3, 1),  # 138
    ChInfo("BIR_8_-4", "BIR4C15", -4, 8, "BIR", 2, 4, 27, 4, 30, 10, 2, 3, 4, 1),  # 139
    ChInfo("BIR_6_5", "BIR5A11", 5, 6, "BIR", 2, 4, 21, 4, 24, 8, 1, 3, 4, 1),  # 140
    ChInfo("BIR_8_5", "BIR5A15", 5, 8, "BIR", 2, 4, 21, 4, 24, 8, 1, 4, 3, 1),  # 141
    ChInfo("BIR_6_-5", "BIR5C11", -5, 6, "BIR", 2, 4, 21, 4, 24, 8, 2, 4, 3, 1),  # 142
    ChInfo("BIR_8_-5", "BIR5C15", -5, 8, "BIR", 2, 4, 21, 4, 24, 8, 2, 3, 4, 1),  # 143
    ChInfo("BIR_6_6", "BIR6A11", 6, 6, "BIR", 2, 4, 36, 4, 36, 12, 1, 3, 4, 1),  # 144
    ChInfo("BIR_8_6", "BIR6A15", 6, 8, "BIR", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 145
    ChInfo("BIR_6_-6", "BIR6C11", -6, 6, "BIR", 2, 4, 36, 4, 36, 12, 2, 4, 3, 1),  # 146
    ChInfo("BIR_8_-6", "BIR6C15", -6, 8, "BIR", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 147
    ChInfo("BIS_1_1", "BIS1A02", 1, 1, "BIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 148
    ChInfo("BIS_2_1", "BIS1A04", 1, 2, "BIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 149
    ChInfo("BIS_3_1", "BIS1A06", 1, 3, "BIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 150
    ChInfo("BIS_4_1", "BIS1A08", 1, 4, "BIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 151
    ChInfo("BIS_5_1", "BIS1A10", 1, 5, "BIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 152
    ChInfo("BIS_6_1", "BIS1A12", 1, 6, "BIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 153
    ChInfo("BIS_7_1", "BIS1A14", 1, 7, "BIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 154
    ChInfo("BIS_8_1", "BIS1A16", 1, 8, "BIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 155
    ChInfo("BIS_1_-1", "BIS1C02", -1, 1, "BIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 156
    ChInfo("BIS_2_-1", "BIS1C04", -1, 2, "BIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 157
    ChInfo("BIS_3_-1", "BIS1C06", -1, 3, "BIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 158
    ChInfo("BIS_4_-1", "BIS1C08", -1, 4, "BIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 159
    ChInfo("BIS_5_-1", "BIS1C10", -1, 5, "BIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 160
    ChInfo("BIS_6_-1", "BIS1C12", -1, 6, "BIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 161
    ChInfo("BIS_7_-1", "BIS1C14", -1, 7, "BIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 162
    ChInfo("BIS_8_-1", "BIS1C16", -1, 8, "BIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 163
    ChInfo("BIS_1_2", "BIS2A02", 2, 1, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 164
    ChInfo("BIS_2_2", "BIS2A04", 2, 2, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 165
    ChInfo("BIS_3_2", "BIS2A06", 2, 3, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 166
    ChInfo("BIS_4_2", "BIS2A08", 2, 4, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 167
    ChInfo("BIS_5_2", "BIS2A10", 2, 5, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 168
    ChInfo("BIS_6_2", "BIS2A12", 2, 6, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 169
    ChInfo("BIS_7_2", "BIS2A14", 2, 7, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 170
    ChInfo("BIS_8_2", "BIS2A16", 2, 8, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 171
    ChInfo("BIS_1_-2", "BIS2C02", -2, 1, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 172
    ChInfo("BIS_2_-2", "BIS2C04", -2, 2, "BIS", 2, 4, 30, 4, 30, 10, 2, 4, 3, 1),  # 173
    ChInfo("BIS_3_-2", "BIS2C06", -2, 3, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 174
    ChInfo("BIS_4_-2", "BIS2C08", -2, 4, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 175
    ChInfo("BIS_5_-2", "BIS2C10", -2, 5, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 176
    ChInfo("BIS_6_-2", "BIS2C12", -2, 6, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 177
    ChInfo("BIS_7_-2", "BIS2C14", -2, 7, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 178
    ChInfo("BIS_8_-2", "BIS2C16", -2, 8, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 179
    ChInfo("BIS_1_3", "BIS3A02", 3, 1, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 180
    ChInfo("BIS_2_3", "BIS3A04", 3, 2, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 181
    ChInfo("BIS_3_3", "BIS3A06", 3, 3, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 182
    ChInfo("BIS_4_3", "BIS3A08", 3, 4, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 183
    ChInfo("BIS_5_3", "BIS3A10", 3, 5, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 184
    ChInfo("BIS_6_3", "BIS3A12", 3, 6, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 185
    ChInfo("BIS_7_3", "BIS3A14", 3, 7, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 186
    ChInfo("BIS_8_3", "BIS3A16", 3, 8, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 187
    ChInfo("BIS_1_-3", "BIS3C02", -3, 1, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 188
    ChInfo("BIS_2_-3", "BIS3C04", -3, 2, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 189
    ChInfo("BIS_3_-3", "BIS3C06", -3, 3, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 190
    ChInfo("BIS_4_-3", "BIS3C08", -3, 4, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 191
    ChInfo("BIS_5_-3", "BIS3C10", -3, 5, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 192
    ChInfo("BIS_6_-3", "BIS3C12", -3, 6, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 193
    ChInfo("BIS_7_-3", "BIS3C14", -3, 7, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 194
    ChInfo("BIS_8_-3", "BIS3C16", -3, 8, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 195
    ChInfo("BIS_1_4", "BIS4A02", 4, 1, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 196
    ChInfo("BIS_2_4", "BIS4A04", 4, 2, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 197
    ChInfo("BIS_3_4", "BIS4A06", 4, 3, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 198
    ChInfo("BIS_4_4", "BIS4A08", 4, 4, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 199
    ChInfo("BIS_5_4", "BIS4A10", 4, 5, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 200
    ChInfo("BIS_6_4", "BIS4A12", 4, 6, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 201
    ChInfo("BIS_7_4", "BIS4A14", 4, 7, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 202
    ChInfo("BIS_8_4", "BIS4A16", 4, 8, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 203
    ChInfo("BIS_1_-4", "BIS4C02", -4, 1, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 204
    ChInfo("BIS_2_-4", "BIS4C04", -4, 2, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 205
    ChInfo("BIS_3_-4", "BIS4C06", -4, 3, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 206
    ChInfo("BIS_4_-4", "BIS4C08", -4, 4, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 207
    ChInfo("BIS_5_-4", "BIS4C10", -4, 5, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 208
    ChInfo("BIS_6_-4", "BIS4C12", -4, 6, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 209
    ChInfo("BIS_7_-4", "BIS4C14", -4, 7, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 210
    ChInfo("BIS_8_-4", "BIS4C16", -4, 8, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 211
    ChInfo("BIS_1_5", "BIS5A02", 5, 1, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 212
    ChInfo("BIS_2_5", "BIS5A04", 5, 2, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 213
    ChInfo("BIS_3_5", "BIS5A06", 5, 3, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 214
    ChInfo("BIS_4_5", "BIS5A08", 5, 4, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 215
    ChInfo("BIS_5_5", "BIS5A10", 5, 5, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 216
    ChInfo("BIS_6_5", "BIS5A12", 5, 6, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 217
    ChInfo("BIS_7_5", "BIS5A14", 5, 7, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 218
    ChInfo("BIS_8_5", "BIS5A16", 5, 8, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 219
    ChInfo("BIS_1_-5", "BIS5C02", -5, 1, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 220
    ChInfo("BIS_2_-5", "BIS5C04", -5, 2, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 221
    ChInfo("BIS_3_-5", "BIS5C06", -5, 3, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 222
    ChInfo("BIS_4_-5", "BIS5C08", -5, 4, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 223
    ChInfo("BIS_5_-5", "BIS5C10", -5, 5, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 224
    ChInfo("BIS_6_-5", "BIS5C12", -5, 6, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 225
    ChInfo("BIS_7_-5", "BIS5C14", -5, 7, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 226
    ChInfo("BIS_8_-5", "BIS5C16", -5, 8, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 227
    ChInfo("BIS_1_6", "BIS6A02", 6, 1, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 228
    ChInfo("BIS_2_6", "BIS6A04", 6, 2, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 229
    ChInfo("BIS_3_6", "BIS6A06", 6, 3, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 230
    ChInfo("BIS_4_6", "BIS6A08", 6, 4, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 231
    ChInfo("BIS_5_6", "BIS6A10", 6, 5, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 232
    ChInfo("BIS_6_6", "BIS6A12", 6, 6, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 233
    ChInfo("BIS_7_6", "BIS6A14", 6, 7, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 234
    ChInfo("BIS_8_6", "BIS6A16", 6, 8, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 235
    ChInfo("BIS_1_-6", "BIS6C02", -6, 1, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 236
    ChInfo("BIS_2_-6", "BIS6C04", -6, 2, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 237
    ChInfo("BIS_3_-6", "BIS6C06", -6, 3, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 238
    ChInfo("BIS_4_-6", "BIS6C08", -6, 4, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 239
    ChInfo("BIS_5_-6", "BIS6C10", -6, 5, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 240
    ChInfo("BIS_6_-6", "BIS6C12", -6, 6, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 241
    ChInfo("BIS_7_-6", "BIS6C14", -6, 7, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 242
    ChInfo("BIS_8_-6", "BIS6C16", -6, 8, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 243
    ChInfo("BIS_1_7", "BIS7A02", 7, 1, "BIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 244
    ChInfo("BIS_2_7", "BIS7A04", 7, 2, "BIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 245
    ChInfo("BIS_3_7", "BIS7A06", 7, 3, "BIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 246
    ChInfo("BIS_4_7", "BIS7A08", 7, 4, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 247
    ChInfo("BIS_5_7", "BIS7A10", 7, 5, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 248
    ChInfo("BIS_6_7", "BIS7A12", 7, 6, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 249
    ChInfo("BIS_7_7", "BIS7A14", 7, 7, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 250
    ChInfo("BIS_8_7", "BIS7A16", 7, 8, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 251
    ChInfo("BIS_1_-7", "BIS7C02", -7, 1, "BIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 252
    ChInfo("BIS_2_-7", "BIS7C04", -7, 2, "BIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 253
    ChInfo("BIS_3_-7", "BIS7C06", -7, 3, "BIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 254
    ChInfo("BIS_4_-7", "BIS7C08", -7, 4, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 255
    ChInfo("BIS_5_-7", "BIS7C10", -7, 5, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 256
    ChInfo("BIS_6_-7", "BIS7C12", -7, 6, "BIS", 2, 4, 30, 4, 30, 10, 2, 3, 4, 1),  # 257
    ChInfo("BIS_7_-7", "BIS7C14", -7, 7, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 258
    ChInfo("BIS_8_-7", "BIS7C16", -7, 8, "BIS", 2, 4, 30, 4, 30, 10, 1, 4, 3, 1),  # 259
    ChInfo("BIS_1_8", "BIS8A02", 8, 1, "BIS", 1, 3, 16, 0, 0, 2, 1, 2, 0, 1),  # 260
    ChInfo("BIS_2_8", "BIS8A04", 8, 2, "BIS", 1, 3, 16, 0, 0, 2, 1, 2, 0, 1),  # 261
    ChInfo("BIS_3_8", "BIS8A06", 8, 3, "BIS", 1, 3, 16, 0, 0, 2, 1, 2, 0, 1),  # 262
    ChInfo("BIS_4_8", "BIS8A08", 8, 4, "BIS", 1, 3, 16, 0, 0, 2, 1, 2, 0, 1),  # 263
    ChInfo("BIS_5_8", "BIS8A10", 8, 5, "BIS", 1, 3, 16, 0, 0, 2, 1, 2, 0, 1),  # 264
    ChInfo("BIS_6_8", "BIS8A12", 8, 6, "BIS", 1, 3, 16, 0, 0, 2, 1, 2, 0, 1),  # 265
    ChInfo("BIS_7_8", "BIS8A14", 8, 7, "BIS", 1, 3, 16, 0, 0, 2, 1, 2, 0, 1),  # 266
    ChInfo("BIS_8_8", "BIS8A16", 8, 8, "BIS", 1, 3, 16, 0, 0, 2, 1, 2, 0, 1),  # 267
    ChInfo("BIS_1_-8", "BIS8C02", -8, 1, "BIS", 1, 3, 16, 0, 0, 2, 1, 1, 0, 1),  # 268
    ChInfo("BIS_2_-8", "BIS8C04", -8, 2, "BIS", 1, 3, 16, 0, 0, 2, 1, 1, 0, 1),  # 269
    ChInfo("BIS_3_-8", "BIS8C06", -8, 3, "BIS", 1, 3, 16, 0, 0, 2, 1, 1, 0, 1),  # 270
    ChInfo("BIS_4_-8", "BIS8C08", -8, 4, "BIS", 1, 3, 16, 0, 0, 2, 1, 1, 0, 1),  # 271
    ChInfo("BIS_5_-8", "BIS8C10", -8, 5, "BIS", 1, 3, 16, 0, 0, 2, 1, 1, 0, 1),  # 272
    ChInfo("BIS_6_-8", "BIS8C12", -8, 6, "BIS", 1, 3, 16, 0, 0, 2, 1, 1, 0, 1),  # 273
    ChInfo("BIS_7_-8", "BIS8C14", -8, 7, "BIS", 1, 3, 16, 0, 0, 2, 1, 1, 0, 1),  # 274
    ChInfo("BIS_8_-8", "BIS8C16", -8, 8, "BIS", 1, 3, 16, 0, 0, 2, 1, 1, 0, 1),  # 275
    ChInfo("BME_7_1", "BME4A13", 1, 7, "BME", 2, 4, 78, 4, 78, 26, 1, 6, 6, 1),  # 276 sMDT
    ChInfo("BME_7_-1", "BME4C13", -1, 7, "BME", 2, 4, 78, 4, 78, 26, 2, 5, 5, 1),  # 277 sMDT
    ChInfo("BMF_6_1", "BMF1A12", 1, 6, "BMF", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 278
    ChInfo("BMF_7_1", "BMF1A14", 1, 7, "BMF", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 279
    ChInfo("BMF_6_-1", "BMF1C12", -1, 6, "BMF", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 280
    ChInfo("BMF_7_-1", "BMF1C14", -1, 7, "BMF", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 281
    ChInfo("BMF_6_2", "BMF2A12", 2, 6, "BMF", 2, 3, 64, 3, 64, 16, 2, 1, 2, 1),  # 282
    ChInfo("BMF_7_2", "BMF2A14", 2, 7, "BMF", 2, 3, 64, 3, 64, 16, 2, 1, 2, 1),  # 283
    ChInfo("BMF_6_-2", "BMF2C12", -2, 6, "BMF", 2, 3, 64, 3, 64, 16, 1, 2, 1, 1),  # 284
    ChInfo("BMF_7_-2", "BMF2C14", -2, 7, "BMF", 2, 3, 64, 3, 64, 16, 1, 2, 1, 1),  # 285
    ChInfo("BMF_6_3", "BMF3A12", 3, 6, "BMF", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 286
    ChInfo("BMF_7_3", "BMF3A14", 3, 7, "BMF", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 287
    ChInfo("BMF_6_-3", "BMF3C12", -3, 6, "BMF", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 288
    ChInfo("BMF_7_-3", "BMF3C14", -3, 7, "BMF", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 289
    ChInfo("BMG_6_1", "BMG2A12", 1, 6, "BMG", 2, 4, 54, 4, 54, 18, 2, 1, 2, 1),  # 290 sMDT
    ChInfo("BMG_7_1", "BMG2A14", 1, 7, "BMG", 2, 4, 54, 4, 54, 18, 2, 1, 2, 1),  # 291 sMDT
    ChInfo("BMG_6_-1", "BMG2C12", -1, 6, "BMG", 2, 4, 54, 4, 54, 18, 2, 1, 2, 1),  # 292 sMDT
    ChInfo("BMG_7_-1", "BMG2C14", -1, 7, "BMG", 2, 4, 54, 4, 54, 18, 2, 1, 2, 1),  # 293 sMDT
    ChInfo("BMG_6_2", "BMG4A12", 2, 6, "BMG", 2, 4, 54, 4, 54, 18, 2, 1, 2, 1),  # 294 sMDT
    ChInfo("BMG_7_2", "BMG4A14", 2, 7, "BMG", 2, 4, 54, 4, 54, 18, 2, 1, 2, 1),  # 295 sMDT
    ChInfo("BMG_6_-2", "BMG4C12", -2, 6, "BMG", 2, 4, 54, 4, 54, 18, 2, 1, 2, 1),  # 296 sMDT
    ChInfo("BMG_7_-2", "BMG4C14", -2, 7, "BMG", 2, 4, 54, 4, 54, 18, 2, 1, 2, 1),  # 297 sMDT
    ChInfo("BMG_6_3", "BMG6A12", 3, 6, "BMG", 2, 4, 54, 4, 54, 18, 2, 1, 2, 1),  # 298 sMDT
    ChInfo("BMG_7_3", "BMG6A14", 3, 7, "BMG", 2, 4, 54, 4, 54, 18, 2, 1, 2, 1),  # 299 sMDT
    ChInfo("BMG_6_-3", "BMG6C12", -3, 6, "BMG", 2, 4, 54, 4, 54, 18, 2, 1, 2, 1),  # 300 sMDT
    ChInfo("BMG_7_-3", "BMG6C14", -3, 7, "BMG", 2, 4, 54, 4, 54, 18, 2, 1, 2, 1),  # 301 sMDT
    ChInfo("BML_1_1", "BML1A01", 1, 1, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 302
    ChInfo("BML_2_1", "BML1A03", 1, 2, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 303
    ChInfo("BML_3_1", "BML1A05", 1, 3, "BML", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 304
    ChInfo("BML_4_1", "BML1A07", 1, 4, "BML", 2, 3, 32, 3, 32, 8, 1, 2, 1, 1),  # 305
    ChInfo("BML_5_1", "BML1A09", 1, 5, "BML", 2, 3, 32, 3, 32, 8, 1, 2, 1, 1),  # 306
    ChInfo("BML_6_1", "BML1A11", 1, 6, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 307
    ChInfo("BML_7_1", "BML1A13", 1, 7, "BML", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 308
    ChInfo("BML_8_1", "BML1A15", 1, 8, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 309
    ChInfo("BML_1_-1", "BML1C01", -1, 1, "BML", 2, 3, 32, 3, 32, 8, 2, 1, 2, 1),  # 310
    ChInfo("BML_2_-1", "BML1C03", -1, 2, "BML", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 311
    ChInfo("BML_3_-1", "BML1C05", -1, 3, "BML", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 312
    ChInfo("BML_4_-1", "BML1C07", -1, 4, "BML", 2, 3, 32, 3, 32, 8, 2, 1, 2, 1),  # 313
    ChInfo("BML_5_-1", "BML1C09", -1, 5, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 314
    ChInfo("BML_6_-1", "BML1C11", -1, 6, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 315
    ChInfo("BML_7_-1", "BML1C13", -1, 7, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 316
    ChInfo("BML_8_-1", "BML1C15", -1, 8, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 317
    ChInfo("BML_1_2", "BML2A01", 2, 1, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 318
    ChInfo("BML_2_2", "BML2A03", 2, 2, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 319
    ChInfo("BML_3_2", "BML2A05", 2, 3, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 320
    ChInfo("BML_4_2", "BML2A07", 2, 4, "BML", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 321
    ChInfo("BML_5_2", "BML2A09", 2, 5, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 322
    ChInfo("BML_6_2", "BML2A11", 2, 6, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 323
    ChInfo("BML_7_2", "BML2A13", 2, 7, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 324
    ChInfo("BML_8_2", "BML2A15", 2, 8, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 325
    ChInfo("BML_1_-2", "BML2C01", -2, 1, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 326
    ChInfo("BML_2_-2", "BML2C03", -2, 2, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 327
    ChInfo("BML_3_-2", "BML2C05", -2, 3, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 328
    ChInfo("BML_4_-2", "BML2C07", -2, 4, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 329
    ChInfo("BML_5_-2", "BML2C09", -2, 5, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 330
    ChInfo("BML_6_-2", "BML2C11", -2, 6, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 331
    ChInfo("BML_7_-2", "BML2C13", -2, 7, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 332
    ChInfo("BML_8_-2", "BML2C15", -2, 8, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 333
    ChInfo("BML_1_3", "BML3A01", 3, 1, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 334
    ChInfo("BML_2_3", "BML3A03", 3, 2, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 335
    ChInfo("BML_3_3", "BML3A05", 3, 3, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 336
    ChInfo("BML_4_3", "BML3A07", 3, 4, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 337
    ChInfo("BML_5_3", "BML3A09", 3, 5, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 338
    ChInfo("BML_6_3", "BML3A11", 3, 6, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 339
    ChInfo("BML_7_3", "BML3A13", 3, 7, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 340
    ChInfo("BML_8_3", "BML3A15", 3, 8, "BML", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 341
    ChInfo("BML_1_-3", "BML3C01", -3, 1, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 342
    ChInfo("BML_2_-3", "BML3C03", -3, 2, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 343
    ChInfo("BML_3_-3", "BML3C05", -3, 3, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 344
    ChInfo("BML_4_-3", "BML3C07", -3, 4, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 345
    ChInfo("BML_5_-3", "BML3C09", -3, 5, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 346
    ChInfo("BML_6_-3", "BML3C11", -3, 6, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 347
    ChInfo("BML_7_-3", "BML3C13", -3, 7, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 348
    ChInfo("BML_8_-3", "BML3C15", -3, 8, "BML", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 349
    ChInfo("BML_1_4", "BML4A01", 4, 1, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 350
    ChInfo("BML_2_4", "BML4A03", 4, 2, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 351
    ChInfo("BML_3_4", "BML4A05", 4, 3, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 352
    ChInfo("BML_4_4", "BML4A07", 4, 4, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 353
    ChInfo("BML_5_4", "BML4A09", 4, 5, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 354
    ChInfo("BML_6_4", "BML4A11", 4, 6, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 355
    ChInfo("BML_8_4", "BML4A15", 4, 8, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 356
    ChInfo("BML_1_-4", "BML4C01", -4, 1, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 357
    ChInfo("BML_2_-4", "BML4C03", -4, 2, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 358
    ChInfo("BML_3_-4", "BML4C05", -4, 3, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 359
    ChInfo("BML_4_-4", "BML4C07", -4, 4, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 360
    ChInfo("BML_5_-4", "BML4C09", -4, 5, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 361
    ChInfo("BML_6_-4", "BML4C11", -4, 6, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 362
    ChInfo("BML_8_-4", "BML4C15", -4, 8, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 363
    ChInfo("BML_1_5", "BML5A01", 5, 1, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 364
    ChInfo("BML_2_5", "BML5A03", 5, 2, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 365
    ChInfo("BML_3_5", "BML5A05", 5, 3, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 366
    ChInfo("BML_4_5", "BML5A07", 5, 4, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 367
    ChInfo("BML_5_5", "BML5A09", 5, 5, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 368
    ChInfo("BML_6_5", "BML5A11", 5, 6, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 369
    ChInfo("BML_7_4", "BML5A13", 4, 7, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 370
    ChInfo("BML_8_5", "BML5A15", 5, 8, "BML", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 371
    ChInfo("BML_1_-5", "BML5C01", -5, 1, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 372
    ChInfo("BML_2_-5", "BML5C03", -5, 2, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 373
    ChInfo("BML_3_-5", "BML5C05", -5, 3, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 374
    ChInfo("BML_4_-5", "BML5C07", -5, 4, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 375
    ChInfo("BML_5_-5", "BML5C09", -5, 5, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 376
    ChInfo("BML_6_-5", "BML5C11", -5, 6, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 377
    ChInfo("BML_7_-4", "BML5C13", -4, 7, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 378
    ChInfo("BML_8_-5", "BML5C15", -5, 8, "BML", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 379
    ChInfo("BML_1_6", "BML6A01", 6, 1, "BML", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 380
    ChInfo("BML_2_6", "BML6A03", 6, 2, "BML", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 381
    ChInfo("BML_3_6", "BML6A05", 6, 3, "BML", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 382
    ChInfo("BML_4_6", "BML6A07", 6, 4, "BML", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 383
    ChInfo("BML_5_6", "BML6A09", 6, 5, "BML", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 384
    ChInfo("BML_6_6", "BML6A11", 6, 6, "BML", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 385
    ChInfo("BML_7_5", "BML6A13", 5, 7, "BML", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 386
    ChInfo("BML_8_6", "BML6A15", 6, 8, "BML", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 387
    ChInfo("BML_1_-6", "BML6C01", -6, 1, "BML", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 388
    ChInfo("BML_2_-6", "BML6C03", -6, 2, "BML", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 389
    ChInfo("BML_3_-6", "BML6C05", -6, 3, "BML", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 390
    ChInfo("BML_4_-6", "BML6C07", -6, 4, "BML", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 391
    ChInfo("BML_5_-6", "BML6C09", -6, 5, "BML", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 392
    ChInfo("BML_6_-6", "BML6C11", -6, 6, "BML", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 393
    ChInfo("BML_7_-5", "BML6C13", -5, 7, "BML", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 394
    ChInfo("BML_8_-6", "BML6C15", -6, 8, "BML", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 395
    ChInfo("BMS_1_1", "BMS1A02", 1, 1, "BMS", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 396
    ChInfo("BMS_2_1", "BMS1A04", 1, 2, "BMS", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 397
    ChInfo("BMS_3_1", "BMS1A06", 1, 3, "BMS", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 398
    ChInfo("BMS_4_1", "BMS1A08", 1, 4, "BMS", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 399
    ChInfo("BMS_5_1", "BMS1A10", 1, 5, "BMS", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 400
    ChInfo("BMS_8_1", "BMS1A16", 1, 8, "BMS", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 401
    ChInfo("BMS_1_-1", "BMS1C02", -1, 1, "BMS", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 402
    ChInfo("BMS_2_-1", "BMS1C04", -1, 2, "BMS", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 403
    ChInfo("BMS_3_-1", "BMS1C06", -1, 3, "BMS", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 404
    ChInfo("BMS_4_-1", "BMS1C08", -1, 4, "BMS", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 405
    ChInfo("BMS_5_-1", "BMS1C10", -1, 5, "BMS", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 406
    ChInfo("BMS_8_-1", "BMS1C16", -1, 8, "BMS", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 407
    ChInfo("BMS_1_2", "BMS2A02", 2, 1, "BMS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 408
    ChInfo("BMS_2_2", "BMS2A04", 2, 2, "BMS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 409
    ChInfo("BMS_3_2", "BMS2A06", 2, 3, "BMS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 410
    ChInfo("BMS_4_2", "BMS2A08", 2, 4, "BMS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 411
    ChInfo("BMS_5_2", "BMS2A10", 2, 5, "BMS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 412
    ChInfo("BMS_8_2", "BMS2A16", 2, 8, "BMS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 413
    ChInfo("BMS_1_-2", "BMS2C02", -2, 1, "BMS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 414
    ChInfo("BMS_2_-2", "BMS2C04", -2, 2, "BMS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 415
    ChInfo("BMS_3_-2", "BMS2C06", -2, 3, "BMS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 416
    ChInfo("BMS_4_-2", "BMS2C08", -2, 4, "BMS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 417
    ChInfo("BMS_5_-2", "BMS2C10", -2, 5, "BMS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 418
    ChInfo("BMS_8_-2", "BMS2C16", -2, 8, "BMS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 419
    ChInfo("BMS_1_3", "BMS3A02", 3, 1, "BMS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 420
    ChInfo("BMS_2_3", "BMS3A04", 3, 2, "BMS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 421
    ChInfo("BMS_3_3", "BMS3A06", 3, 3, "BMS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 422
    ChInfo("BMS_4_3", "BMS3A08", 3, 4, "BMS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 423
    ChInfo("BMS_5_3", "BMS3A10", 3, 5, "BMS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 424
    ChInfo("BMS_8_3", "BMS3A16", 3, 8, "BMS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 425
    ChInfo("BMS_1_-3", "BMS3C02", -3, 1, "BMS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 426
    ChInfo("BMS_2_-3", "BMS3C04", -3, 2, "BMS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 427
    ChInfo("BMS_3_-3", "BMS3C06", -3, 3, "BMS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 428
    ChInfo("BMS_4_-3", "BMS3C08", -3, 4, "BMS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 429
    ChInfo("BMS_5_-3", "BMS3C10", -3, 5, "BMS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 430
    ChInfo("BMS_8_-3", "BMS3C16", -3, 8, "BMS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 431
    ChInfo("BMS_1_4", "BMS4A02", 4, 1, "BMS", 2, 3, 40, 3, 48, 11, 2, 1, 2, 1),  # 432
    ChInfo("BMS_2_4", "BMS4A04", 4, 2, "BMS", 2, 3, 40, 3, 48, 11, 2, 1, 2, 1),  # 433
    ChInfo("BMS_3_4", "BMS4A06", 4, 3, "BMS", 2, 3, 40, 3, 48, 11, 2, 1, 2, 1),  # 434
    ChInfo("BMS_4_4", "BMS4A08", 4, 4, "BMS", 2, 3, 40, 3, 48, 11, 2, 1, 2, 1),  # 435
    ChInfo("BMS_5_4", "BMS4A10", 4, 5, "BMS", 2, 3, 40, 3, 48, 11, 2, 1, 2, 1),  # 436
    ChInfo("BMS_8_4", "BMS4A16", 4, 8, "BMS", 2, 3, 40, 3, 48, 11, 2, 1, 2, 1),  # 437
    ChInfo("BMS_1_-4", "BMS4C02", -4, 1, "BMS", 2, 3, 40, 3, 48, 11, 1, 2, 1, 1),  # 438
    ChInfo("BMS_2_-4", "BMS4C04", -4, 2, "BMS", 2, 3, 40, 3, 48, 11, 1, 2, 1, 1),  # 439
    ChInfo("BMS_3_-4", "BMS4C06", -4, 3, "BMS", 2, 3, 40, 3, 48, 11, 1, 2, 1, 1),  # 440
    ChInfo("BMS_4_-4", "BMS4C08", -4, 4, "BMS", 2, 3, 40, 3, 48, 11, 1, 2, 1, 1),  # 441
    ChInfo("BMS_5_-4", "BMS4C10", -4, 5, "BMS", 2, 3, 40, 3, 48, 11, 1, 2, 1, 1),  # 442
    ChInfo("BMS_8_-4", "BMS4C16", -4, 8, "BMS", 2, 3, 40, 3, 48, 11, 1, 2, 1, 1),  # 443
    ChInfo("BMS_1_5", "BMS5A02", 5, 1, "BMS", 2, 3, 32, 3, 32, 8, 2, 1, 2, 1),  # 444
    ChInfo("BMS_2_5", "BMS5A04", 5, 2, "BMS", 2, 3, 32, 3, 32, 8, 2, 1, 2, 1),  # 445
    ChInfo("BMS_3_5", "BMS5A06", 5, 3, "BMS", 2, 3, 32, 3, 32, 8, 2, 1, 2, 1),  # 446
    ChInfo("BMS_4_5", "BMS5A08", 5, 4, "BMS", 2, 3, 32, 3, 32, 8, 2, 1, 2, 1),  # 447
    ChInfo("BMS_5_5", "BMS5A10", 5, 5, "BMS", 2, 3, 32, 3, 32, 8, 2, 1, 2, 1),  # 448
    ChInfo("BMS_8_5", "BMS5A16", 5, 8, "BMS", 2, 3, 32, 3, 32, 8, 2, 1, 2, 1),  # 449
    ChInfo("BMS_1_-5", "BMS5C02", -5, 1, "BMS", 2, 3, 32, 3, 32, 8, 1, 2, 1, 1),  # 450
    ChInfo("BMS_2_-5", "BMS5C04", -5, 2, "BMS", 2, 3, 32, 3, 32, 8, 1, 2, 1, 1),  # 451
    ChInfo("BMS_3_-5", "BMS5C06", -5, 3, "BMS", 2, 3, 32, 3, 32, 8, 1, 2, 1, 1),  # 452
    ChInfo("BMS_4_-5", "BMS5C08", -5, 4, "BMS", 2, 3, 32, 3, 32, 8, 1, 2, 1, 1),  # 453
    ChInfo("BMS_5_-5", "BMS5C10", -5, 5, "BMS", 2, 3, 32, 3, 32, 8, 1, 2, 1, 1),  # 454
    ChInfo("BMS_8_-5", "BMS5C16", -5, 8, "BMS", 2, 3, 32, 3, 32, 8, 1, 2, 1, 1),  # 455
    ChInfo("BMS_1_6", "BMS6A02", 6, 1, "BMS", 2, 3, 40, 3, 48, 11, 2, 1, 2, 1),  # 456
    ChInfo("BMS_2_6", "BMS6A04", 6, 2, "BMS", 2, 3, 40, 3, 48, 11, 2, 1, 2, 1),  # 457
    ChInfo("BMS_3_6", "BMS6A06", 6, 3, "BMS", 2, 3, 40, 3, 48, 11, 2, 1, 2, 1),  # 458
    ChInfo("BMS_4_6", "BMS6A08", 6, 4, "BMS", 2, 3, 40, 3, 48, 11, 2, 1, 2, 1),  # 459
    ChInfo("BMS_5_6", "BMS6A10", 6, 5, "BMS", 2, 3, 40, 3, 48, 11, 2, 1, 2, 1),  # 460
    ChInfo("BMS_8_6", "BMS6A16", 6, 8, "BMS", 2, 3, 40, 3, 48, 11, 2, 1, 2, 1),  # 461
    ChInfo("BMS_1_-6", "BMS6C02", -6, 1, "BMS", 2, 3, 40, 3, 48, 11, 1, 2, 1, 1),  # 462
    ChInfo("BMS_2_-6", "BMS6C04", -6, 2, "BMS", 2, 3, 40, 3, 48, 11, 1, 2, 1, 1),  # 463
    ChInfo("BMS_3_-6", "BMS6C06", -6, 3, "BMS", 2, 3, 40, 3, 48, 11, 1, 2, 1, 1),  # 464
    ChInfo("BMS_4_-6", "BMS6C08", -6, 4, "BMS", 2, 3, 40, 3, 48, 11, 1, 2, 1, 1),  # 465
    ChInfo("BMS_5_-6", "BMS6C10", -6, 5, "BMS", 2, 3, 40, 3, 48, 11, 1, 2, 1, 1),  # 466
    ChInfo("BMS_8_-6", "BMS6C16", -6, 8, "BMS", 2, 3, 40, 3, 48, 11, 1, 2, 1, 1),  # 467
    ChInfo("BOF_6_1", "BOF1A12", 1, 6, "BOF", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 468
    ChInfo("BOF_7_1", "BOF1A14", 1, 7, "BOF", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 469
    ChInfo("BOF_6_-1", "BOF1C12", -1, 6, "BOF", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 470
    ChInfo("BOF_7_-1", "BOF1C14", -1, 7, "BOF", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 471
    ChInfo("BOF_6_2", "BOF3A12", 2, 6, "BOF", 2, 3, 64, 3, 64, 16, 2, 1, 2, 1),  # 472
    ChInfo("BOF_7_2", "BOF3A14", 2, 7, "BOF", 2, 3, 64, 3, 64, 16, 1, 2, 1, 1),  # 473
    ChInfo("BOF_6_-2", "BOF3C12", -2, 6, "BOF", 2, 3, 64, 3, 64, 16, 1, 2, 1, 1),  # 474
    ChInfo("BOF_7_-2", "BOF3C14", -2, 7, "BOF", 2, 3, 64, 3, 64, 16, 2, 1, 2, 1),  # 475
    ChInfo("BOF_6_3", "BOF5A12", 3, 6, "BOF", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 476
    ChInfo("BOF_7_3", "BOF5A14", 3, 7, "BOF", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 477
    ChInfo("BOF_6_-3", "BOF5C12", -3, 6, "BOF", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 478
    ChInfo("BOF_7_-3", "BOF5C14", -3, 7, "BOF", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 479
    ChInfo("BOF_6_4", "BOF7A12", 4, 6, "BOF", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 480
    ChInfo("BOF_7_4", "BOF7A14", 4, 7, "BOF", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 481
    ChInfo("BOF_6_-4", "BOF7C12", -4, 6, "BOF", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 482
    ChInfo("BOF_7_-4", "BOF7C14", -4, 7, "BOF", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 483
    ChInfo("BOG_6_0", "BOG0A12", 0, 6, "BOG", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 484
    ChInfo("BOG_7_0", "BOG0A14", 0, 7, "BOG", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 485
    ChInfo("BOG_6_1", "BOG2A12", 1, 6, "BOG", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 486
    ChInfo("BOG_7_1", "BOG2A14", 1, 7, "BOG", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 487
    ChInfo("BOG_6_-1", "BOG2C12", -1, 6, "BOG", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 488
    ChInfo("BOG_7_-1", "BOG2C14", -1, 7, "BOG", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 489
    ChInfo("BOG_6_2", "BOG4A12", 2, 6, "BOG", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 490
    ChInfo("BOG_7_2", "BOG4A14", 2, 7, "BOG", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 491
    ChInfo("BOG_6_-2", "BOG4C12", -2, 6, "BOG", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 492
    ChInfo("BOG_7_-2", "BOG4C14", -2, 7, "BOG", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 493
    ChInfo("BOG_6_3", "BOG6A12", 3, 6, "BOG", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 494
    ChInfo("BOG_7_3", "BOG6A14", 3, 7, "BOG", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 495
    ChInfo("BOG_6_-3", "BOG6C12", -3, 6, "BOG", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 496
    ChInfo("BOG_7_-3", "BOG6C14", -3, 7, "BOG", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 497
    ChInfo("BOG_6_4", "BOG8A12", 4, 6, "BOG", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 498
    ChInfo("BOG_7_4", "BOG8A14", 4, 7, "BOG", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 499
    ChInfo("BOG_6_-4", "BOG8C12", -4, 6, "BOG", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 500
    ChInfo("BOG_7_-4", "BOG8C14", -4, 7, "BOG", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 501
    ChInfo("BOL_1_1", "BOL1A01", 1, 1, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 502
    ChInfo("BOL_2_1", "BOL1A03", 1, 2, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 503
    ChInfo("BOL_3_1", "BOL1A05", 1, 3, "BOL", 2, 3, 64, 3, 64, 16, 1, 2, 1, 1),  # 504
    ChInfo("BOL_4_1", "BOL1A07", 1, 4, "BOL", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 505
    ChInfo("BOL_5_1", "BOL1A09", 1, 5, "BOL", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 506
    ChInfo("BOL_6_1", "BOL1A11", 1, 6, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 507
    ChInfo("BOL_7_1", "BOL1A13", 1, 7, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 508
    ChInfo("BOL_8_1", "BOL1A15", 1, 8, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 509
    ChInfo("BOL_1_-1", "BOL1C01", -1, 1, "BOL", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 510
    ChInfo("BOL_2_-1", "BOL1C03", -1, 2, "BOL", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 511
    ChInfo("BOL_3_-1", "BOL1C05", -1, 3, "BOL", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 512
    ChInfo("BOL_4_-1", "BOL1C07", -1, 4, "BOL", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 513
    ChInfo("BOL_5_-1", "BOL1C09", -1, 5, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 514
    ChInfo("BOL_6_-1", "BOL1C11", -1, 6, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 515
    ChInfo("BOL_7_-1", "BOL1C13", -1, 7, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 516
    ChInfo("BOL_8_-1", "BOL1C15", -1, 8, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 517
    ChInfo("BOL_1_2", "BOL2A01", 2, 1, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 518
    ChInfo("BOL_2_2", "BOL2A03", 2, 2, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 519
    ChInfo("BOL_3_2", "BOL2A05", 2, 3, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 520
    ChInfo("BOL_4_2", "BOL2A07", 2, 4, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 521
    ChInfo("BOL_5_2", "BOL2A09", 2, 5, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 522
    ChInfo("BOL_6_2", "BOL2A11", 2, 6, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 523
    ChInfo("BOL_7_2", "BOL2A13", 2, 7, "BOL", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 524
    ChInfo("BOL_8_2", "BOL2A15", 2, 8, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 525
    ChInfo("BOL_1_-2", "BOL2C01", -2, 1, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 526
    ChInfo("BOL_2_-2", "BOL2C03", -2, 2, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 527
    ChInfo("BOL_3_-2", "BOL2C05", -2, 3, "BOL", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 528
    ChInfo("BOL_4_-2", "BOL2C07", -2, 4, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 529
    ChInfo("BOL_5_-2", "BOL2C09", -2, 5, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 530
    ChInfo("BOL_6_-2", "BOL2C11", -2, 6, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 531
    ChInfo("BOL_7_-2", "BOL2C13", -2, 7, "BOL", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 532
    ChInfo("BOL_8_-2", "BOL2C15", -2, 8, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 533
    ChInfo("BOL_1_3", "BOL3A01", 3, 1, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 534
    ChInfo("BOL_2_3", "BOL3A03", 3, 2, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 535
    ChInfo("BOL_3_3", "BOL3A05", 3, 3, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 536
    ChInfo("BOL_4_3", "BOL3A07", 3, 4, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 537
    ChInfo("BOL_5_3", "BOL3A09", 3, 5, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 538
    ChInfo("BOL_6_3", "BOL3A11", 3, 6, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 539
    ChInfo("BOL_7_3", "BOL3A13", 3, 7, "BOL", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 540
    ChInfo("BOL_8_3", "BOL3A15", 3, 8, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 541
    ChInfo("BOL_1_-3", "BOL3C01", -3, 1, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 542
    ChInfo("BOL_2_-3", "BOL3C03", -3, 2, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 543
    ChInfo("BOL_3_-3", "BOL3C05", -3, 3, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 544
    ChInfo("BOL_4_-3", "BOL3C07", -3, 4, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 545
    ChInfo("BOL_5_-3", "BOL3C09", -3, 5, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 546
    ChInfo("BOL_6_-3", "BOL3C11", -3, 6, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 547
    ChInfo("BOL_7_-3", "BOL3C13", -3, 7, "BOL", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 548
    ChInfo("BOL_8_-3", "BOL3C15", -3, 8, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 549
    ChInfo("BOL_1_4", "BOL4A01", 4, 1, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 550
    ChInfo("BOL_2_4", "BOL4A03", 4, 2, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 551
    ChInfo("BOL_3_4", "BOL4A05", 4, 3, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 552
    ChInfo("BOL_4_4", "BOL4A07", 4, 4, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 553
    ChInfo("BOL_5_4", "BOL4A09", 4, 5, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 554
    ChInfo("BOL_6_4", "BOL4A11", 4, 6, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 555
    ChInfo("BOL_7_4", "BOL4A13", 4, 7, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 556
    ChInfo("BOL_8_4", "BOL4A15", 4, 8, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 557
    ChInfo("BOL_1_-4", "BOL4C01", -4, 1, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 558
    ChInfo("BOL_2_-4", "BOL4C03", -4, 2, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 559
    ChInfo("BOL_3_-4", "BOL4C05", -4, 3, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 560
    ChInfo("BOL_4_-4", "BOL4C07", -4, 4, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 561
    ChInfo("BOL_5_-4", "BOL4C09", -4, 5, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 562
    ChInfo("BOL_6_-4", "BOL4C11", -4, 6, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 563
    ChInfo("BOL_7_-4", "BOL4C13", -4, 7, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 564
    ChInfo("BOL_8_-4", "BOL4C15", -4, 8, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 565
    ChInfo("BOL_1_5", "BOL5A01", 5, 1, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 566
    ChInfo("BOL_2_5", "BOL5A03", 5, 2, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 567
    ChInfo("BOL_3_5", "BOL5A05", 5, 3, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 568
    ChInfo("BOL_4_5", "BOL5A07", 5, 4, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 569
    ChInfo("BOL_5_5", "BOL5A09", 5, 5, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 570
    ChInfo("BOL_6_5", "BOL5A11", 5, 6, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 571
    ChInfo("BOL_7_5", "BOL5A13", 5, 7, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 572
    ChInfo("BOL_8_5", "BOL5A15", 5, 8, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 573
    ChInfo("BOL_1_-5", "BOL5C01", -5, 1, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 574
    ChInfo("BOL_2_-5", "BOL5C03", -5, 2, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 575
    ChInfo("BOL_3_-5", "BOL5C05", -5, 3, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 576
    ChInfo("BOL_4_-5", "BOL5C07", -5, 4, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 577
    ChInfo("BOL_5_-5", "BOL5C09", -5, 5, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 578
    ChInfo("BOL_6_-5", "BOL5C11", -5, 6, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 579
    ChInfo("BOL_7_-5", "BOL5C13", -5, 7, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 580
    ChInfo("BOL_8_-5", "BOL5C15", -5, 8, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 581
    ChInfo("BOL_1_6", "BOL6A01", 6, 1, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 582
    ChInfo("BOL_2_6", "BOL6A03", 6, 2, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 583
    ChInfo("BOL_3_6", "BOL6A05", 6, 3, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 584
    ChInfo("BOL_4_6", "BOL6A07", 6, 4, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 585
    ChInfo("BOL_5_6", "BOL6A09", 6, 5, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 586
    ChInfo("BOL_6_6", "BOL6A11", 6, 6, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 587
    ChInfo("BOL_7_6", "BOL6A13", 6, 7, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 588
    ChInfo("BOL_8_6", "BOL6A15", 6, 8, "BOL", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 589
    ChInfo("BOL_7_7", "BOE3A13", 7, 7, "BOL", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 590
    ChInfo("BOL_1_-6", "BOL6C01", -6, 1, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 591
    ChInfo("BOL_2_-6", "BOL6C03", -6, 2, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 592
    ChInfo("BOL_3_-6", "BOL6C05", -6, 3, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 593
    ChInfo("BOL_4_-6", "BOL6C07", -6, 4, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 594
    ChInfo("BOL_5_-6", "BOL6C09", -6, 5, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 595
    ChInfo("BOL_6_-6", "BOL6C11", -6, 6, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 596
    ChInfo("BOL_7_-6", "BOL6C13", -6, 7, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 597
    ChInfo("BOL_8_-6", "BOL6C15", -6, 8, "BOL", 2, 3, 56, 3, 56, 14, 2, 1, 2, 1),  # 598
    ChInfo("BOL_7_-7", "BOE3C13", -7, 7, "BOL", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 599
    ChInfo("BOS_1_1", "BOS1A02", 1, 1, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 600
    ChInfo("BOS_2_1", "BOS1A04", 1, 2, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 601
    ChInfo("BOS_3_1", "BOS1A06", 1, 3, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 602
    ChInfo("BOS_4_1", "BOS1A08", 1, 4, "BOS", 2, 3, 48, 3, 48, 12, 2, 1, 2, 1),  # 603
    ChInfo("BOS_5_1", "BOS1A10", 1, 5, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 604
    ChInfo("BOS_8_1", "BOS1A16", 1, 8, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 605
    ChInfo("BOS_1_-1", "BOS1C02", -1, 1, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 606
    ChInfo("BOS_2_-1", "BOS1C04", -1, 2, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 607
    ChInfo("BOS_3_-1", "BOS1C06", -1, 3, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 608
    ChInfo("BOS_4_-1", "BOS1C08", -1, 4, "BOS", 2, 3, 48, 3, 48, 12, 1, 2, 1, 1),  # 609
    ChInfo("BOS_5_-1", "BOS1C10", -1, 5, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 610
    ChInfo("BOS_8_-1", "BOS1C16", -1, 8, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 611
    ChInfo("BOS_1_2", "BOS2A02", 2, 1, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 612
    ChInfo("BOS_2_2", "BOS2A04", 2, 2, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 613
    ChInfo("BOS_3_2", "BOS2A06", 2, 3, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 614
    ChInfo("BOS_4_2", "BOS2A08", 2, 4, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 615
    ChInfo("BOS_5_2", "BOS2A10", 2, 5, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 616
    ChInfo("BOS_8_2", "BOS2A16", 2, 8, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 617
    ChInfo("BOS_1_-2", "BOS2C02", -2, 1, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 618
    ChInfo("BOS_2_-2", "BOS2C04", -2, 2, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 619
    ChInfo("BOS_3_-2", "BOS2C06", -2, 3, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 620
    ChInfo("BOS_4_-2", "BOS2C08", -2, 4, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 621
    ChInfo("BOS_5_-2", "BOS2C10", -2, 5, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 622
    ChInfo("BOS_8_-2", "BOS2C16", -2, 8, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 623
    ChInfo("BOS_1_3", "BOS3A02", 3, 1, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 624
    ChInfo("BOS_2_3", "BOS3A04", 3, 2, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 625
    ChInfo("BOS_3_3", "BOS3A06", 3, 3, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 626
    ChInfo("BOS_4_3", "BOS3A08", 3, 4, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 627
    ChInfo("BOS_5_3", "BOS3A10", 3, 5, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 628
    ChInfo("BOS_8_3", "BOS3A16", 3, 8, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 629
    ChInfo("BOS_1_-3", "BOS3C02", -3, 1, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 630
    ChInfo("BOS_2_-3", "BOS3C04", -3, 2, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 631
    ChInfo("BOS_3_-3", "BOS3C06", -3, 3, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 632
    ChInfo("BOS_4_-3", "BOS3C08", -3, 4, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 633
    ChInfo("BOS_5_-3", "BOS3C10", -3, 5, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 634
    ChInfo("BOS_8_-3", "BOS3C16", -3, 8, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 635
    ChInfo("BOS_1_4", "BOS4A02", 4, 1, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 636
    ChInfo("BOS_2_4", "BOS4A04", 4, 2, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 637
    ChInfo("BOS_3_4", "BOS4A06", 4, 3, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 638
    ChInfo("BOS_4_4", "BOS4A08", 4, 4, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 639
    ChInfo("BOS_5_4", "BOS4A10", 4, 5, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 640
    ChInfo("BOS_8_4", "BOS4A16", 4, 8, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 641
    ChInfo("BOS_1_-4", "BOS4C02", -4, 1, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 642
    ChInfo("BOS_2_-4", "BOS4C04", -4, 2, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 643
    ChInfo("BOS_3_-4", "BOS4C06", -4, 3, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 644
    ChInfo("BOS_4_-4", "BOS4C08", -4, 4, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 645
    ChInfo("BOS_5_-4", "BOS4C10", -4, 5, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 646
    ChInfo("BOS_8_-4", "BOS4C16", -4, 8, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 647
    ChInfo("BOS_1_5", "BOS5A02", 5, 1, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 648
    ChInfo("BOS_2_5", "BOS5A04", 5, 2, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 649
    ChInfo("BOS_3_5", "BOS5A06", 5, 3, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 650
    ChInfo("BOS_4_5", "BOS5A08", 5, 4, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 651
    ChInfo("BOS_5_5", "BOS5A10", 5, 5, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 652
    ChInfo("BOS_8_5", "BOS5A16", 5, 8, "BOS", 2, 3, 72, 3, 72, 18, 2, 1, 2, 1),  # 653
    ChInfo("BOS_1_-5", "BOS5C02", -5, 1, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 654
    ChInfo("BOS_2_-5", "BOS5C04", -5, 2, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 655
    ChInfo("BOS_3_-5", "BOS5C06", -5, 3, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 656
    ChInfo("BOS_4_-5", "BOS5C08", -5, 4, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 657
    ChInfo("BOS_5_-5", "BOS5C10", -5, 5, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 658
    ChInfo("BOS_8_-5", "BOS5C16", -5, 8, "BOS", 2, 3, 72, 3, 72, 18, 1, 2, 1, 1),  # 659
    ChInfo("BOS_1_6", "BOS6A02", 6, 1, "BOS", 2, 3, 64, 3, 64, 16, 2, 1, 2, 1),  # 660
    ChInfo("BOS_2_6", "BOS6A04", 6, 2, "BOS", 2, 3, 64, 3, 64, 16, 2, 1, 2, 1),  # 661
    ChInfo("BOS_3_6", "BOS6A06", 6, 3, "BOS", 2, 3, 64, 3, 64, 16, 2, 1, 2, 1),  # 662
    ChInfo("BOS_4_6", "BOS6A08", 6, 4, "BOS", 2, 3, 64, 3, 64, 16, 2, 1, 2, 1),  # 663
    ChInfo("BOS_5_6", "BOS6A10", 6, 5, "BOS", 2, 3, 64, 3, 64, 16, 2, 1, 2, 1),  # 664
    ChInfo("BOS_8_6", "BOS6A16", 6, 8, "BOS", 2, 3, 64, 3, 64, 16, 2, 1, 2, 1),  # 665
    ChInfo("BOS_1_-6", "BOS6C02", -6, 1, "BOS", 2, 3, 64, 3, 64, 16, 1, 2, 1, 1),  # 666
    ChInfo("BOS_2_-6", "BOS6C04", -6, 2, "BOS", 2, 3, 64, 3, 64, 16, 1, 2, 1, 1),  # 667
    ChInfo("BOS_3_-6", "BOS6C06", -6, 3, "BOS", 2, 3, 64, 3, 64, 16, 1, 2, 1, 1),  # 668
    ChInfo("BOS_4_-6", "BOS6C08", -6, 4, "BOS", 2, 3, 64, 3, 64, 16, 1, 2, 1, 1),  # 669
    ChInfo("BOS_5_-6", "BOS6C10", -6, 5, "BOS", 2, 3, 64, 3, 64, 16, 1, 2, 1, 1),  # 670
    ChInfo("BOS_8_-6", "BOS6C16", -6, 8, "BOS", 2, 3, 64, 3, 64, 16, 1, 2, 1, 1),  # 671
    ChInfo("EEL_1_1", "EEL1A01", 1, 1, "EEL", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),
    # 672 ML1 tube was 48, but this is wrong!
    ChInfo("EEL_2_1", "EEL1A03", 1, 2, "EEL", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 673
    ChInfo("EEL_4_1", "EEL1A07", 1, 4, "EEL", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 674
    ChInfo("EEL_5_1", "EEL1A09", 1, 5, "EEL", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 675
    ChInfo("EEL_6_1", "EEL1A11", 1, 6, "EEL", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 676
    ChInfo("EEL_7_1", "EEL1A13", 1, 7, "EEL", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 677
    ChInfo("EEL_8_1", "EEL1A15", 1, 8, "EEL", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 678
    ChInfo("EEL_1_-1", "EEL1C01", -1, 1, "EEL", 2, 3, 40, 3, 40, 10, 2, 1, 2, 1),  # 679
    ChInfo("EEL_2_-1", "EEL1C03", -1, 2, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 680
    ChInfo("EEL_4_-1", "EEL1C07", -1, 4, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 681
    ChInfo("EEL_5_-1", "EEL1C09", -1, 5, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 682
    ChInfo("EEL_6_-1", "EEL1C11", -1, 6, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 683
    ChInfo("EEL_7_-1", "EEL1C13", -1, 7, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 684
    ChInfo("EEL_8_-1", "EEL1C15", -1, 8, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 685
    ChInfo("EEL_1_2", "EEL2A01", 2, 1, "EEL", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 686
    ChInfo("EEL_2_2", "EEL2A03", 2, 2, "EEL", 2, 3, 40, 3, 40, 10, 1, 2, 1, 1),  # 687
    ChInfo("EEL_3_1", "EEL2A05", 1, 3, "EEL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 688
    ChInfo("EEL_4_2", "EEL2A07", 2, 4, "EEL", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 689
    ChInfo("EEL_5_2", "EEL2A09", 2, 5, "EEL", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 690
    ChInfo("EEL_6_2", "EEL2A11", 2, 6, "EEL", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 691
    ChInfo("EEL_7_2", "EEL2A13", 2, 7, "EEL", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 692
    ChInfo("EEL_8_2", "EEL2A15", 2, 8, "EEL", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 693
    ChInfo("EEL_1_-2", "EEL2C01", -2, 1, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 694
    ChInfo("EEL_2_-2", "EEL2C03", -2, 2, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 695
    ChInfo("EEL_3_-1", "EEL2C05", -1, 3, "EEL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 696
    ChInfo("EEL_4_-2", "EEL2C07", -2, 4, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 697
    ChInfo("EEL_5_-2", "EEL2C09", -2, 5, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 698
    ChInfo("EEL_6_-2", "EEL2C11", -2, 6, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 699
    ChInfo("EEL_7_-2", "EEL2C13", -2, 7, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 700
    ChInfo("EEL_8_-2", "EEL2C15", -2, 8, "EEL", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 701
    ChInfo("EES_1_1", "EES1A02", 1, 1, "EES", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 702
    ChInfo("EES_2_1", "EES1A04", 1, 2, "EES", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 703
    ChInfo("EES_3_1", "EES1A06", 1, 3, "EES", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 704
    ChInfo("EES_4_1", "EES1A08", 1, 4, "EES", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 705
    ChInfo("EES_5_1", "EES1A10", 1, 5, "EES", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 706
    ChInfo("EES_6_1", "EES1A12", 1, 6, "EES", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 707
    ChInfo("EES_7_1", "EES1A14", 1, 7, "EES", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 708
    ChInfo("EES_8_1", "EES1A16", 1, 8, "EES", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 709
    ChInfo("EES_1_-1", "EES1C02", -1, 1, "EES", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 710
    ChInfo("EES_2_-1", "EES1C04", -1, 2, "EES", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 711
    ChInfo("EES_3_-1", "EES1C06", -1, 3, "EES", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 712
    ChInfo("EES_4_-1", "EES1C08", -1, 4, "EES", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 713
    ChInfo("EES_5_-1", "EES1C10", -1, 5, "EES", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 714
    ChInfo("EES_6_-1", "EES1C12", -1, 6, "EES", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 715
    ChInfo("EES_7_-1", "EES1C14", -1, 7, "EES", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 716
    ChInfo("EES_8_-1", "EES1C16", -1, 8, "EES", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 717
    ChInfo("EES_1_2", "EES2A02", 2, 1, "EES", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 718
    ChInfo("EES_2_2", "EES2A04", 2, 2, "EES", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 719
    ChInfo("EES_3_2", "EES2A06", 2, 3, "EES", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 720
    ChInfo("EES_4_2", "EES2A08", 2, 4, "EES", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 721
    ChInfo("EES_5_2", "EES2A10", 2, 5, "EES", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 722
    ChInfo("EES_6_2", "EES2A12", 2, 6, "EES", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 723
    ChInfo("EES_7_2", "EES2A14", 2, 7, "EES", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 724
    ChInfo("EES_8_2", "EES2A16", 2, 8, "EES", 2, 3, 40, 3, 40, 10, 1, 1, 2, 1),  # 725
    ChInfo("EES_1_-2", "EES2C02", -2, 1, "EES", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 726
    ChInfo("EES_2_-2", "EES2C04", -2, 2, "EES", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 727
    ChInfo("EES_3_-2", "EES2C06", -2, 3, "EES", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 728
    ChInfo("EES_4_-2", "EES2C08", -2, 4, "EES", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 729
    ChInfo("EES_5_-2", "EES2C10", -2, 5, "EES", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 730
    ChInfo("EES_6_-2", "EES2C12", -2, 6, "EES", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 731
    ChInfo("EES_7_-2", "EES2C14", -2, 7, "EES", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 732
    ChInfo("EES_8_-2", "EES2C16", -2, 8, "EES", 2, 3, 40, 3, 40, 10, 2, 2, 1, 1),  # 733
    ChInfo("EIL_1_1", "EIL1A01", 1, 1, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 734
    ChInfo("EIL_2_1", "EIL1A03", 1, 2, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 735
    ChInfo("EIL_3_1", "EIL1A05", 1, 3, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 736
    ChInfo("EIL_4_1", "EIL1A07", 1, 4, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 737
    ChInfo("EIL_5_1", "EIL1A09", 1, 5, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 738
    ChInfo("EIL_6_1", "EIL1A11", 1, 6, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 739
    ChInfo("EIL_7_1", "EIL1A13", 1, 7, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 740
    ChInfo("EIL_8_1", "EIL1A15", 1, 8, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 741
    ChInfo("EIL_1_-1", "EIL1C01", -1, 1, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 742
    ChInfo("EIL_2_-1", "EIL1C03", -1, 2, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 743
    ChInfo("EIL_3_-1", "EIL1C05", -1, 3, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 744
    ChInfo("EIL_4_-1", "EIL1C07", -1, 4, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 745
    ChInfo("EIL_5_-1", "EIL1C09", -1, 5, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 746
    ChInfo("EIL_6_-1", "EIL1C11", -1, 6, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 747
    ChInfo("EIL_7_-1", "EIL1C13", -1, 7, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 748
    ChInfo("EIL_8_-1", "EIL1C15", -1, 8, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 749
    ChInfo("EIL_1_2", "EIL2A01", 2, 1, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 750
    ChInfo("EIL_2_2", "EIL2A03", 2, 2, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 751
    ChInfo("EIL_3_2", "EIL2A05", 2, 3, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 752
    ChInfo("EIL_4_2", "EIL2A07", 2, 4, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 753
    ChInfo("EIL_5_2", "EIL2A09", 2, 5, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 754
    ChInfo("EIL_6_2", "EIL2A11", 2, 6, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 755
    ChInfo("EIL_7_2", "EIL2A13", 2, 7, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 756
    ChInfo("EIL_8_2", "EIL2A15", 2, 8, "EIL", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 757
    ChInfo("EIL_1_-2", "EIL2C01", -2, 1, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 758
    ChInfo("EIL_2_-2", "EIL2C03", -2, 2, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 759
    ChInfo("EIL_3_-2", "EIL2C05", -2, 3, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 760
    ChInfo("EIL_4_-2", "EIL2C07", -2, 4, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 761
    ChInfo("EIL_5_-2", "EIL2C09", -2, 5, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 762
    ChInfo("EIL_6_-2", "EIL2C11", -2, 6, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 763
    ChInfo("EIL_7_-2", "EIL2C13", -2, 7, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 764
    ChInfo("EIL_8_-2", "EIL2C15", -2, 8, "EIL", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 765
    ChInfo("EIL_1_3", "EIL3A01", 3, 1, "EIL", 2, 4, 12, 4, 12, 4, 2, 3, 4, 1),  # 766
    ChInfo("EIL_2_3", "EIL3A03", 3, 2, "EIL", 2, 4, 12, 4, 12, 4, 2, 3, 4, 1),  # 767
    ChInfo("EIL_3_3", "EIL3A05", 3, 3, "EIL", 2, 4, 12, 4, 12, 4, 2, 3, 4, 1),  # 768
    ChInfo("EIL_4_3", "EIL3A07", 3, 4, "EIL", 2, 4, 12, 4, 12, 4, 2, 3, 4, 1),  # 769
    ChInfo("EIL_5_3", "EIL3A09", 3, 5, "EIL", 2, 4, 12, 4, 12, 4, 2, 3, 4, 1),  # 770
    ChInfo("EIL_6_3", "EIL3A11", 3, 6, "EIL", 2, 4, 12, 4, 12, 4, 2, 3, 4, 1),  # 771
    ChInfo("EIL_7_3", "EIL3A13", 3, 7, "EIL", 2, 4, 12, 4, 12, 4, 2, 3, 4, 1),  # 772
    ChInfo("EIL_8_3", "EIL3A15", 3, 8, "EIL", 2, 4, 12, 4, 12, 4, 2, 3, 4, 1),  # 773
    ChInfo("EIL_1_-3", "EIL3C01", -3, 1, "EIL", 2, 4, 12, 4, 12, 4, 1, 4, 3, 1),  # 774
    ChInfo("EIL_2_-3", "EIL3C03", -3, 2, "EIL", 2, 4, 12, 4, 12, 4, 1, 4, 3, 1),  # 775
    ChInfo("EIL_3_-3", "EIL3C05", -3, 3, "EIL", 2, 4, 12, 4, 12, 4, 1, 4, 3, 1),  # 776
    ChInfo("EIL_4_-3", "EIL3C07", -3, 4, "EIL", 2, 4, 12, 4, 12, 4, 1, 4, 3, 1),  # 777
    ChInfo("EIL_5_-3", "EIL3C09", -3, 5, "EIL", 2, 4, 12, 4, 12, 4, 1, 4, 3, 1),  # 778
    ChInfo("EIL_6_-3", "EIL3C11", -3, 6, "EIL", 2, 4, 12, 4, 12, 4, 1, 4, 3, 1),  # 779
    ChInfo("EIL_7_-3", "EIL3C13", -3, 7, "EIL", 2, 4, 12, 4, 12, 4, 1, 4, 3, 1),  # 780
    ChInfo("EIL_8_-3", "EIL3C15", -3, 8, "EIL", 2, 4, 12, 4, 12, 4, 1, 4, 3, 1),  # 781
    ChInfo("EIL_1_4", "EIL4A01", 4, 1, "EIL", 2, 4, 12, 4, 12, 4, 1, 5, 6, 1),  # 782
    ChInfo("EIL_2_4", "EIL4A03", 4, 2, "EIL", 2, 4, 54, 4, 54, 18, 1, 4, 3, 1),  # 783
    ChInfo("EIL_3_4", "EIL4A05", 4, 3, "EIL", 2, 4, 54, 4, 54, 18, 1, 4, 3, 1),  # 784
    ChInfo("EIL_4_4", "EIL4A07", 4, 4, "EIL", 2, 4, 54, 4, 54, 18, 1, 4, 3, 1),  # 785
    ChInfo("EIL_5_4", "EIL4A09", 4, 5, "EIL", 2, 4, 12, 4, 12, 4, 1, 5, 6, 1),  # 786
    ChInfo("EIL_6_4", "EIL4A11", 4, 6, "EIL", 2, 4, 42, 4, 42, 14, 1, 4, 3, 1),  # 787
    ChInfo("EIL_7_4", "EIL4A13", 4, 7, "EIL", 2, 4, 54, 4, 54, 18, 1, 4, 3, 1),  # 788
    ChInfo("EIL_8_4", "EIL4A15", 4, 8, "EIL", 2, 4, 42, 4, 42, 14, 1, 4, 3, 1),  # 789
    ChInfo("EIL_1_-4", "EIL4C01", -4, 1, "EIL", 2, 4, 12, 4, 12, 4, 2, 5, 6, 1),  # 790
    ChInfo("EIL_2_-4", "EIL4C03", -4, 2, "EIL", 2, 4, 54, 4, 54, 18, 2, 3, 4, 1),  # 791
    ChInfo("EIL_3_-4", "EIL4C05", -4, 3, "EIL", 2, 4, 54, 4, 54, 18, 2, 3, 4, 1),  # 792
    ChInfo("EIL_4_-4", "EIL4C07", -4, 4, "EIL", 2, 4, 54, 4, 54, 18, 2, 3, 4, 1),  # 793
    ChInfo("EIL_5_-4", "EIL4C09", -4, 5, "EIL", 2, 4, 12, 4, 12, 4, 2, 5, 6, 1),  # 794
    ChInfo("EIL_6_-4", "EIL4C11", -4, 6, "EIL", 2, 4, 42, 4, 42, 14, 2, 3, 4, 1),  # 795
    ChInfo("EIL_7_-4", "EIL4C13", -4, 7, "EIL", 2, 4, 54, 4, 54, 18, 2, 3, 4, 1),  # 796
    ChInfo("EIL_8_-4", "EIL4C15", -4, 8, "EIL", 2, 4, 42, 4, 42, 14, 2, 3, 4, 1),  # 797
    ChInfo("EIL_1_5", "EIL5A01", 5, 1, "EIL", 2, 4, 42, 4, 42, 14, 1, 4, 3, 1),  # 798
    ChInfo("EIL_5_5", "EIL5A09", 5, 5, "EIL", 2, 4, 42, 4, 42, 14, 1, 4, 3, 1),  # 799
    ChInfo("EIL_1_-5", "EIL5C01", -5, 1, "EIL", 2, 4, 42, 4, 42, 14, 2, 3, 4, 1),  # 800
    ChInfo("EIL_5_-5", "EIL5C09", -5, 5, "EIL", 2, 4, 42, 4, 42, 14, 2, 3, 4, 1),  # 801
    ChInfo("EIS_1_1", "EIS1A02", 1, 1, "EIS", 2, 4, 42, 4, 42, 14, 1, 4, 3, 1),  # 802
    ChInfo("EIS_2_1", "EIS1A04", 1, 2, "EIS", 2, 4, 42, 4, 42, 14, 1, 4, 3, 1),  # 803
    ChInfo("EIS_3_1", "EIS1A06", 1, 3, "EIS", 2, 4, 42, 4, 42, 14, 1, 4, 3, 1),  # 804
    ChInfo("EIS_4_1", "EIS1A08", 1, 4, "EIS", 2, 4, 42, 4, 42, 14, 1, 4, 3, 1),  # 805
    ChInfo("EIS_5_1", "EIS1A10", 1, 5, "EIS", 2, 4, 42, 4, 42, 14, 1, 4, 3, 1),  # 806
    ChInfo("EIS_6_1", "EIS1A12", 1, 6, "EIS", 2, 4, 42, 4, 42, 14, 1, 4, 3, 1),  # 807
    ChInfo("EIS_7_1", "EIS1A14", 1, 7, "EIS", 2, 4, 42, 4, 42, 14, 1, 4, 3, 1),  # 808
    ChInfo("EIS_8_1", "EIS1A16", 1, 8, "EIS", 2, 4, 42, 4, 42, 14, 1, 4, 3, 1),  # 809
    ChInfo("EIS_1_-1", "EIS1C02", -1, 1, "EIS", 2, 4, 42, 4, 42, 14, 2, 3, 4, 1),  # 810
    ChInfo("EIS_2_-1", "EIS1C04", -1, 2, "EIS", 2, 4, 42, 4, 42, 14, 2, 3, 4, 1),  # 811
    ChInfo("EIS_3_-1", "EIS1C06", -1, 3, "EIS", 2, 4, 42, 4, 42, 14, 2, 3, 4, 1),  # 812
    ChInfo("EIS_4_-1", "EIS1C08", -1, 4, "EIS", 2, 4, 42, 4, 42, 14, 2, 3, 4, 1),  # 813
    ChInfo("EIS_5_-1", "EIS1C10", -1, 5, "EIS", 2, 4, 42, 4, 42, 14, 2, 3, 4, 1),  # 814
    ChInfo("EIS_6_-1", "EIS1C12", -1, 6, "EIS", 2, 4, 42, 4, 42, 14, 2, 3, 4, 1),  # 815
    ChInfo("EIS_7_-1", "EIS1C14", -1, 7, "EIS", 2, 4, 42, 4, 42, 14, 2, 3, 4, 1),  # 816
    ChInfo("EIS_8_-1", "EIS1C16", -1, 8, "EIS", 2, 4, 42, 4, 42, 14, 2, 3, 4, 1),  # 817
    ChInfo("EIS_1_2", "EIS2A02", 2, 1, "EIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 818
    ChInfo("EIS_2_2", "EIS2A04", 2, 2, "EIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 819
    ChInfo("EIS_3_2", "EIS2A06", 2, 3, "EIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 820
    ChInfo("EIS_4_2", "EIS2A08", 2, 4, "EIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 821
    ChInfo("EIS_5_2", "EIS2A10", 2, 5, "EIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 822
    ChInfo("EIS_6_2", "EIS2A12", 2, 6, "EIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 823
    ChInfo("EIS_7_2", "EIS2A14", 2, 7, "EIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 824
    ChInfo("EIS_8_2", "EIS2A16", 2, 8, "EIS", 2, 4, 36, 4, 36, 12, 1, 4, 3, 1),  # 825
    ChInfo("EIS_1_-2", "EIS2C02", -2, 1, "EIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 826
    ChInfo("EIS_2_-2", "EIS2C04", -2, 2, "EIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 827
    ChInfo("EIS_3_-2", "EIS2C06", -2, 3, "EIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 828
    ChInfo("EIS_4_-2", "EIS2C08", -2, 4, "EIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 829
    ChInfo("EIS_5_-2", "EIS2C10", -2, 5, "EIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 830
    ChInfo("EIS_6_-2", "EIS2C12", -2, 6, "EIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 831
    ChInfo("EIS_7_-2", "EIS2C14", -2, 7, "EIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 832
    ChInfo("EIS_8_-2", "EIS2C16", -2, 8, "EIS", 2, 4, 36, 4, 36, 12, 2, 3, 4, 1),  # 833
    ChInfo("EML_1_1", "EML1A01", 1, 1, "EML", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 834
    ChInfo("EML_2_1", "EML1A03", 1, 2, "EML", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 835
    ChInfo("EML_3_1", "EML1A05", 1, 3, "EML", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 836
    ChInfo("EML_4_1", "EML1A07", 1, 4, "EML", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 837
    ChInfo("EML_5_1", "EML1A09", 1, 5, "EML", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 838
    ChInfo("EML_6_1", "EML1A11", 1, 6, "EML", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 839
    ChInfo("EML_7_1", "EML1A13", 1, 7, "EML", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 840
    ChInfo("EML_8_1", "EML1A15", 1, 8, "EML", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 841
    ChInfo("EML_1_-1", "EML1C01", -1, 1, "EML", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 842
    ChInfo("EML_2_-1", "EML1C03", -1, 2, "EML", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 843
    ChInfo("EML_3_-1", "EML1C05", -1, 3, "EML", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 844
    ChInfo("EML_4_-1", "EML1C07", -1, 4, "EML", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 845
    ChInfo("EML_5_-1", "EML1C09", -1, 5, "EML", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 846
    ChInfo("EML_6_-1", "EML1C11", -1, 6, "EML", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 847
    ChInfo("EML_7_-1", "EML1C13", -1, 7, "EML", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 848
    ChInfo("EML_8_-1", "EML1C15", -1, 8, "EML", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 849
    ChInfo("EML_1_2", "EML2A01", 2, 1, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 850
    ChInfo("EML_2_2", "EML2A03", 2, 2, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 851
    ChInfo("EML_3_2", "EML2A05", 2, 3, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 852
    ChInfo("EML_4_2", "EML2A07", 2, 4, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 853
    ChInfo("EML_5_2", "EML2A09", 2, 5, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 854
    ChInfo("EML_6_2", "EML2A11", 2, 6, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 855
    ChInfo("EML_7_2", "EML2A13", 2, 7, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 856
    ChInfo("EML_8_2", "EML2A15", 2, 8, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 857
    ChInfo("EML_1_-2", "EML2C01", -2, 1, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 858
    ChInfo("EML_2_-2", "EML2C03", -2, 2, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 859
    ChInfo("EML_3_-2", "EML2C05", -2, 3, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 860
    ChInfo("EML_4_-2", "EML2C07", -2, 4, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 861
    ChInfo("EML_5_-2", "EML2C09", -2, 5, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 862
    ChInfo("EML_6_-2", "EML2C11", -2, 6, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 863
    ChInfo("EML_7_-2", "EML2C13", -2, 7, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 864
    ChInfo("EML_8_-2", "EML2C15", -2, 8, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 865
    ChInfo("EML_1_3", "EML3A01", 3, 1, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 866
    ChInfo("EML_2_3", "EML3A03", 3, 2, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 867
    ChInfo("EML_3_3", "EML3A05", 3, 3, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 868
    ChInfo("EML_4_3", "EML3A07", 3, 4, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 869
    ChInfo("EML_5_3", "EML3A09", 3, 5, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 870
    ChInfo("EML_6_3", "EML3A11", 3, 6, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 871
    ChInfo("EML_7_3", "EML3A13", 3, 7, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 872
    ChInfo("EML_8_3", "EML3A15", 3, 8, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 873
    ChInfo("EML_1_-3", "EML3C01", -3, 1, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 874
    ChInfo("EML_2_-3", "EML3C03", -3, 2, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 875
    ChInfo("EML_3_-3", "EML3C05", -3, 3, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 876
    ChInfo("EML_4_-3", "EML3C07", -3, 4, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 877
    ChInfo("EML_5_-3", "EML3C09", -3, 5, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 878
    ChInfo("EML_6_-3", "EML3C11", -3, 6, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 879
    ChInfo("EML_7_-3", "EML3C13", -3, 7, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 880
    ChInfo("EML_8_-3", "EML3C15", -3, 8, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 881
    ChInfo("EML_1_4", "EML4A01", 4, 1, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 882
    ChInfo("EML_2_4", "EML4A03", 4, 2, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 883
    ChInfo("EML_3_4", "EML4A05", 4, 3, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 884
    ChInfo("EML_4_4", "EML4A07", 4, 4, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 885
    ChInfo("EML_5_4", "EML4A09", 4, 5, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 886
    ChInfo("EML_6_4", "EML4A11", 4, 6, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 887
    ChInfo("EML_7_4", "EML4A13", 4, 7, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 888
    ChInfo("EML_8_4", "EML4A15", 4, 8, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 889
    ChInfo("EML_1_-4", "EML4C01", -4, 1, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 890
    ChInfo("EML_2_-4", "EML4C03", -4, 2, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 891
    ChInfo("EML_3_-4", "EML4C05", -4, 3, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 892
    ChInfo("EML_4_-4", "EML4C07", -4, 4, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 893
    ChInfo("EML_5_-4", "EML4C09", -4, 5, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 894
    ChInfo("EML_6_-4", "EML4C11", -4, 6, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 895
    ChInfo("EML_7_-4", "EML4C13", -4, 7, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 896
    ChInfo("EML_8_-4", "EML4C15", -4, 8, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 897
    ChInfo("EML_1_5", "EML5A01", 5, 1, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 898
    ChInfo("EML_2_5", "EML5A03", 5, 2, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 899
    ChInfo("EML_3_5", "EML5A05", 5, 3, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 900
    ChInfo("EML_4_5", "EML5A07", 5, 4, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 901
    ChInfo("EML_5_5", "EML5A09", 5, 5, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 902
    ChInfo("EML_6_5", "EML5A11", 5, 6, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 903
    ChInfo("EML_7_5", "EML5A13", 5, 7, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 904
    ChInfo("EML_8_5", "EML5A15", 5, 8, "EML", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 905
    ChInfo("EML_1_-5", "EML5C01", -5, 1, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 906
    ChInfo("EML_2_-5", "EML5C03", -5, 2, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 907
    ChInfo("EML_3_-5", "EML5C05", -5, 3, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 908
    ChInfo("EML_4_-5", "EML5C07", -5, 4, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 909
    ChInfo("EML_5_-5", "EML5C09", -5, 5, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 910
    ChInfo("EML_6_-5", "EML5C11", -5, 6, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 911
    ChInfo("EML_7_-5", "EML5C13", -5, 7, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 912
    ChInfo("EML_8_-5", "EML5C15", -5, 8, "EML", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 913
    ChInfo("EMS_1_1", "EMS1A02", 1, 1, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 914
    ChInfo("EMS_2_1", "EMS1A04", 1, 2, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 915
    ChInfo("EMS_3_1", "EMS1A06", 1, 3, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 916
    ChInfo("EMS_4_1", "EMS1A08", 1, 4, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 917
    ChInfo("EMS_5_1", "EMS1A10", 1, 5, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 918
    ChInfo("EMS_6_1", "EMS1A12", 1, 6, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 919
    ChInfo("EMS_7_1", "EMS1A14", 1, 7, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 920
    ChInfo("EMS_8_1", "EMS1A16", 1, 8, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 921
    ChInfo("EMS_1_-1", "EMS1C02", -1, 1, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 922
    ChInfo("EMS_2_-1", "EMS1C04", -1, 2, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 923
    ChInfo("EMS_3_-1", "EMS1C06", -1, 3, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 924
    ChInfo("EMS_4_-1", "EMS1C08", -1, 4, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 925
    ChInfo("EMS_5_-1", "EMS1C10", -1, 5, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 926
    ChInfo("EMS_6_-1", "EMS1C12", -1, 6, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 927
    ChInfo("EMS_7_-1", "EMS1C14", -1, 7, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 928
    ChInfo("EMS_8_-1", "EMS1C16", -1, 8, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 929
    ChInfo("EMS_1_2", "EMS2A02", 2, 1, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 930
    ChInfo("EMS_2_2", "EMS2A04", 2, 2, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 931
    ChInfo("EMS_3_2", "EMS2A06", 2, 3, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 932
    ChInfo("EMS_4_2", "EMS2A08", 2, 4, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 933
    ChInfo("EMS_5_2", "EMS2A10", 2, 5, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 934
    ChInfo("EMS_6_2", "EMS2A12", 2, 6, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 935
    ChInfo("EMS_7_2", "EMS2A14", 2, 7, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 936
    ChInfo("EMS_8_2", "EMS2A16", 2, 8, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 937
    ChInfo("EMS_1_-2", "EMS2C02", -2, 1, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 938
    ChInfo("EMS_2_-2", "EMS2C04", -2, 2, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 939
    ChInfo("EMS_3_-2", "EMS2C06", -2, 3, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 940
    ChInfo("EMS_4_-2", "EMS2C08", -2, 4, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 941
    ChInfo("EMS_5_-2", "EMS2C10", -2, 5, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 942
    ChInfo("EMS_6_-2", "EMS2C12", -2, 6, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 943
    ChInfo("EMS_7_-2", "EMS2C14", -2, 7, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 944
    ChInfo("EMS_8_-2", "EMS2C16", -2, 8, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 945
    ChInfo("EMS_1_3", "EMS3A02", 3, 1, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 946
    ChInfo("EMS_2_3", "EMS3A04", 3, 2, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 947
    ChInfo("EMS_3_3", "EMS3A06", 3, 3, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 948
    ChInfo("EMS_4_3", "EMS3A08", 3, 4, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 949
    ChInfo("EMS_5_3", "EMS3A10", 3, 5, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 950
    ChInfo("EMS_6_3", "EMS3A12", 3, 6, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 951
    ChInfo("EMS_7_3", "EMS3A14", 3, 7, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 952
    ChInfo("EMS_8_3", "EMS3A16", 3, 8, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 953
    ChInfo("EMS_1_-3", "EMS3C02", -3, 1, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 954
    ChInfo("EMS_2_-3", "EMS3C04", -3, 2, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 955
    ChInfo("EMS_3_-3", "EMS3C06", -3, 3, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 956
    ChInfo("EMS_4_-3", "EMS3C08", -3, 4, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 957
    ChInfo("EMS_5_-3", "EMS3C10", -3, 5, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 958
    ChInfo("EMS_6_-3", "EMS3C12", -3, 6, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 959
    ChInfo("EMS_7_-3", "EMS3C14", -3, 7, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 960
    ChInfo("EMS_8_-3", "EMS3C16", -3, 8, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 961
    ChInfo("EMS_1_4", "EMS4A02", 4, 1, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 962
    ChInfo("EMS_2_4", "EMS4A04", 4, 2, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 963
    ChInfo("EMS_3_4", "EMS4A06", 4, 3, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 964
    ChInfo("EMS_4_4", "EMS4A08", 4, 4, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 965
    ChInfo("EMS_5_4", "EMS4A10", 4, 5, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 966
    ChInfo("EMS_6_4", "EMS4A12", 4, 6, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 967
    ChInfo("EMS_7_4", "EMS4A14", 4, 7, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 968
    ChInfo("EMS_8_4", "EMS4A16", 4, 8, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 969
    ChInfo("EMS_1_-4", "EMS4C02", -4, 1, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 970
    ChInfo("EMS_2_-4", "EMS4C04", -4, 2, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 971
    ChInfo("EMS_3_-4", "EMS4C06", -4, 3, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 972
    ChInfo("EMS_4_-4", "EMS4C08", -4, 4, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 973
    ChInfo("EMS_5_-4", "EMS4C10", -4, 5, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 974
    ChInfo("EMS_6_-4", "EMS4C12", -4, 6, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 975
    ChInfo("EMS_7_-4", "EMS4C14", -4, 7, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 976
    ChInfo("EMS_8_-4", "EMS4C16", -4, 8, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 977
    ChInfo("EMS_1_5", "EMS5A02", 5, 1, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 978
    ChInfo("EMS_2_5", "EMS5A04", 5, 2, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 979
    ChInfo("EMS_3_5", "EMS5A06", 5, 3, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 980
    ChInfo("EMS_4_5", "EMS5A08", 5, 4, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 981
    ChInfo("EMS_5_5", "EMS5A10", 5, 5, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 982
    ChInfo("EMS_6_5", "EMS5A12", 5, 6, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 983
    ChInfo("EMS_7_5", "EMS5A14", 5, 7, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 984
    ChInfo("EMS_8_5", "EMS5A16", 5, 8, "EMS", 2, 3, 64, 3, 64, 16, 1, 1, 2, 1),  # 985
    ChInfo("EMS_1_-5", "EMS5C02", -5, 1, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 986
    ChInfo("EMS_2_-5", "EMS5C04", -5, 2, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 987
    ChInfo("EMS_3_-5", "EMS5C06", -5, 3, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 988
    ChInfo("EMS_4_-5", "EMS5C08", -5, 4, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 989
    ChInfo("EMS_5_-5", "EMS5C10", -5, 5, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 990
    ChInfo("EMS_6_-5", "EMS5C12", -5, 6, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 991
    ChInfo("EMS_7_-5", "EMS5C14", -5, 7, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 992
    ChInfo("EMS_8_-5", "EMS5C16", -5, 8, "EMS", 2, 3, 64, 3, 64, 16, 2, 2, 1, 1),  # 993
    ChInfo("EOL_1_1", "EOL1A01", 1, 1, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 994
    ChInfo("EOL_2_1", "EOL1A03", 1, 2, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 995
    ChInfo("EOL_3_1", "EOL1A05", 1, 3, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 996
    ChInfo("EOL_4_1", "EOL1A07", 1, 4, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 997
    ChInfo("EOL_5_1", "EOL1A09", 1, 5, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 998
    ChInfo("EOL_6_1", "EOL1A11", 1, 6, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 999
    ChInfo("EOL_7_1", "EOL1A13", 1, 7, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1000
    ChInfo("EOL_8_1", "EOL1A15", 1, 8, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1001
    ChInfo("EOL_1_-1", "EOL1C01", -1, 1, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1002
    ChInfo("EOL_2_-1", "EOL1C03", -1, 2, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1003
    ChInfo("EOL_3_-1", "EOL1C05", -1, 3, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1004
    ChInfo("EOL_4_-1", "EOL1C07", -1, 4, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1005
    ChInfo("EOL_5_-1", "EOL1C09", -1, 5, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1006
    ChInfo("EOL_6_-1", "EOL1C11", -1, 6, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1007
    ChInfo("EOL_7_-1", "EOL1C13", -1, 7, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1008
    ChInfo("EOL_8_-1", "EOL1C15", -1, 8, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1009
    ChInfo("EOL_1_2", "EOL2A01", 2, 1, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1010
    ChInfo("EOL_2_2", "EOL2A03", 2, 2, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1011
    ChInfo("EOL_3_2", "EOL2A05", 2, 3, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1012
    ChInfo("EOL_4_2", "EOL2A07", 2, 4, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1013
    ChInfo("EOL_5_2", "EOL2A09", 2, 5, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1014
    ChInfo("EOL_6_2", "EOL2A11", 2, 6, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1015
    ChInfo("EOL_7_2", "EOL2A13", 2, 7, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1016
    ChInfo("EOL_8_2", "EOL2A15", 2, 8, "EOL", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1017
    ChInfo("EOL_1_-2", "EOL2C01", -2, 1, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1018
    ChInfo("EOL_2_-2", "EOL2C03", -2, 2, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1019
    ChInfo("EOL_3_-2", "EOL2C05", -2, 3, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1020
    ChInfo("EOL_4_-2", "EOL2C07", -2, 4, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1021
    ChInfo("EOL_5_-2", "EOL2C09", -2, 5, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1022
    ChInfo("EOL_6_-2", "EOL2C11", -2, 6, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1023
    ChInfo("EOL_7_-2", "EOL2C13", -2, 7, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1024
    ChInfo("EOL_8_-2", "EOL2C15", -2, 8, "EOL", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1025
    ChInfo("EOL_1_3", "EOL3A01", 3, 1, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1026
    ChInfo("EOL_2_3", "EOL3A03", 3, 2, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1027
    ChInfo("EOL_3_3", "EOL3A05", 3, 3, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1028
    ChInfo("EOL_4_3", "EOL3A07", 3, 4, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1029
    ChInfo("EOL_5_3", "EOL3A09", 3, 5, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1030
    ChInfo("EOL_6_3", "EOL3A11", 3, 6, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1031
    ChInfo("EOL_7_3", "EOL3A13", 3, 7, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1032
    ChInfo("EOL_8_3", "EOL3A15", 3, 8, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1033
    ChInfo("EOL_1_-3", "EOL3C01", -3, 1, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1034
    ChInfo("EOL_2_-3", "EOL3C03", -3, 2, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1035
    ChInfo("EOL_3_-3", "EOL3C05", -3, 3, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1036
    ChInfo("EOL_4_-3", "EOL3C07", -3, 4, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1037
    ChInfo("EOL_5_-3", "EOL3C09", -3, 5, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1038
    ChInfo("EOL_6_-3", "EOL3C11", -3, 6, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1039
    ChInfo("EOL_7_-3", "EOL3C13", -3, 7, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1040
    ChInfo("EOL_8_-3", "EOL3C15", -3, 8, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1041
    ChInfo("EOL_1_4", "EOL4A01", 4, 1, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1042
    ChInfo("EOL_2_4", "EOL4A03", 4, 2, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1043
    ChInfo("EOL_3_4", "EOL4A05", 4, 3, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1044
    ChInfo("EOL_4_4", "EOL4A07", 4, 4, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1045
    ChInfo("EOL_5_4", "EOL4A09", 4, 5, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1046
    ChInfo("EOL_6_4", "EOL4A11", 4, 6, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1047
    ChInfo("EOL_7_4", "EOL4A13", 4, 7, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1048
    ChInfo("EOL_8_4", "EOL4A15", 4, 8, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1049
    ChInfo("EOL_1_-4", "EOL4C01", -4, 1, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1050
    ChInfo("EOL_2_-4", "EOL4C03", -4, 2, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1051
    ChInfo("EOL_3_-4", "EOL4C05", -4, 3, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1052
    ChInfo("EOL_4_-4", "EOL4C07", -4, 4, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1053
    ChInfo("EOL_5_-4", "EOL4C09", -4, 5, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1054
    ChInfo("EOL_6_-4", "EOL4C11", -4, 6, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1055
    ChInfo("EOL_7_-4", "EOL4C13", -4, 7, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1056
    ChInfo("EOL_8_-4", "EOL4C15", -4, 8, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1057
    ChInfo("EOL_1_5", "EOL5A01", 5, 1, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1058
    ChInfo("EOL_2_5", "EOL5A03", 5, 2, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1059
    ChInfo("EOL_3_5", "EOL5A05", 5, 3, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1060
    ChInfo("EOL_4_5", "EOL5A07", 5, 4, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1061
    ChInfo("EOL_5_5", "EOL5A09", 5, 5, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1062
    ChInfo("EOL_6_5", "EOL5A11", 5, 6, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1063
    ChInfo("EOL_7_5", "EOL5A13", 5, 7, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1064
    ChInfo("EOL_8_5", "EOL5A15", 5, 8, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1065
    ChInfo("EOL_1_-5", "EOL5C01", -5, 1, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1066
    ChInfo("EOL_2_-5", "EOL5C03", -5, 2, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1067
    ChInfo("EOL_3_-5", "EOL5C05", -5, 3, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1068
    ChInfo("EOL_4_-5", "EOL5C07", -5, 4, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1069
    ChInfo("EOL_5_-5", "EOL5C09", -5, 5, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1070
    ChInfo("EOL_6_-5", "EOL5C11", -5, 6, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1071
    ChInfo("EOL_7_-5", "EOL5C13", -5, 7, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1072
    ChInfo("EOL_8_-5", "EOL5C15", -5, 8, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1073
    ChInfo("EOL_1_6", "EOL6A01", 6, 1, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1074
    ChInfo("EOL_2_6", "EOL6A03", 6, 2, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1075
    ChInfo("EOL_3_6", "EOL6A05", 6, 3, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1076
    ChInfo("EOL_4_6", "EOL6A07", 6, 4, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1077
    ChInfo("EOL_5_6", "EOL6A09", 6, 5, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1078
    ChInfo("EOL_6_6", "EOL6A11", 6, 6, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1079
    ChInfo("EOL_7_6", "EOL6A13", 6, 7, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1080
    ChInfo("EOL_8_6", "EOL6A15", 6, 8, "EOL", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1081
    ChInfo("EOL_1_-6", "EOL6C01", -6, 1, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1082
    ChInfo("EOL_2_-6", "EOL6C03", -6, 2, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1083
    ChInfo("EOL_3_-6", "EOL6C05", -6, 3, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1084
    ChInfo("EOL_4_-6", "EOL6C07", -6, 4, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1085
    ChInfo("EOL_5_-6", "EOL6C09", -6, 5, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1086
    ChInfo("EOL_6_-6", "EOL6C11", -6, 6, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1087
    ChInfo("EOL_7_-6", "EOL6C13", -6, 7, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1088
    ChInfo("EOL_8_-6", "EOL6C15", -6, 8, "EOL", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1089
    ChInfo("EOS_1_1", "EOS1A02", 1, 1, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1090
    ChInfo("EOS_2_1", "EOS1A04", 1, 2, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1091
    ChInfo("EOS_3_1", "EOS1A06", 1, 3, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1092
    ChInfo("EOS_4_1", "EOS1A08", 1, 4, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1093
    ChInfo("EOS_5_1", "EOS1A10", 1, 5, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1094
    ChInfo("EOS_6_1", "EOS1A12", 1, 6, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1095
    ChInfo("EOS_7_1", "EOS1A14", 1, 7, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1096
    ChInfo("EOS_8_1", "EOS1A16", 1, 8, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1097
    ChInfo("EOS_1_-1", "EOS1C02", -1, 1, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1098
    ChInfo("EOS_2_-1", "EOS1C04", -1, 2, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1099
    ChInfo("EOS_3_-1", "EOS1C06", -1, 3, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1100
    ChInfo("EOS_4_-1", "EOS1C08", -1, 4, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1101
    ChInfo("EOS_5_-1", "EOS1C10", -1, 5, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1102
    ChInfo("EOS_6_-1", "EOS1C12", -1, 6, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1103
    ChInfo("EOS_7_-1", "EOS1C14", -1, 7, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1104
    ChInfo("EOS_8_-1", "EOS1C16", -1, 8, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1105
    ChInfo("EOS_1_2", "EOS2A02", 2, 1, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1106
    ChInfo("EOS_2_2", "EOS2A04", 2, 2, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1107
    ChInfo("EOS_3_2", "EOS2A06", 2, 3, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1108
    ChInfo("EOS_4_2", "EOS2A08", 2, 4, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1109
    ChInfo("EOS_5_2", "EOS2A10", 2, 5, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1110
    ChInfo("EOS_6_2", "EOS2A12", 2, 6, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1111
    ChInfo("EOS_7_2", "EOS2A14", 2, 7, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1112
    ChInfo("EOS_8_2", "EOS2A16", 2, 8, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1113
    ChInfo("EOS_1_-2", "EOS2C02", -2, 1, "EOS", 2, 3, 56, 3, 56, 14, 1, 2, 1, 1),  # 1114
    ChInfo("EOS_2_-2", "EOS2C04", -2, 2, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1115
    ChInfo("EOS_3_-2", "EOS2C06", -2, 3, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1116
    ChInfo("EOS_4_-2", "EOS2C08", -2, 4, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1117
    ChInfo("EOS_5_-2", "EOS2C10", -2, 5, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1118
    ChInfo("EOS_6_-2", "EOS2C12", -2, 6, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1119
    ChInfo("EOS_7_-2", "EOS2C14", -2, 7, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1120
    ChInfo("EOS_8_-2", "EOS2C16", -2, 8, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1121
    ChInfo("EOS_1_3", "EOS3A02", 3, 1, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1122
    ChInfo("EOS_2_3", "EOS3A04", 3, 2, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1123
    ChInfo("EOS_3_3", "EOS3A06", 3, 3, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1124
    ChInfo("EOS_4_3", "EOS3A08", 3, 4, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1125
    ChInfo("EOS_5_3", "EOS3A10", 3, 5, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1126
    ChInfo("EOS_6_3", "EOS3A12", 3, 6, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1127
    ChInfo("EOS_7_3", "EOS3A14", 3, 7, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1128
    ChInfo("EOS_8_3", "EOS3A16", 3, 8, "EOS", 2, 3, 56, 3, 56, 14, 1, 1, 2, 1),  # 1129
    ChInfo("EOS_1_-3", "EOS3C02", -3, 1, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1130
    ChInfo("EOS_2_-3", "EOS3C04", -3, 2, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1131
    ChInfo("EOS_3_-3", "EOS3C06", -3, 3, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1132
    ChInfo("EOS_4_-3", "EOS3C08", -3, 4, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1133
    ChInfo("EOS_5_-3", "EOS3C10", -3, 5, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1134
    ChInfo("EOS_6_-3", "EOS3C12", -3, 6, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1135
    ChInfo("EOS_7_-3", "EOS3C14", -3, 7, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1136
    ChInfo("EOS_8_-3", "EOS3C16", -3, 8, "EOS", 2, 3, 56, 3, 56, 14, 2, 2, 1, 1),  # 1137
    ChInfo("EOS_1_4", "EOS4A02", 4, 1, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1138
    ChInfo("EOS_2_4", "EOS4A04", 4, 2, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1139
    ChInfo("EOS_3_4", "EOS4A06", 4, 3, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1140
    ChInfo("EOS_4_4", "EOS4A08", 4, 4, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1141
    ChInfo("EOS_5_4", "EOS4A10", 4, 5, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1142
    ChInfo("EOS_6_4", "EOS4A12", 4, 6, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1143
    ChInfo("EOS_7_4", "EOS4A14", 4, 7, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1144
    ChInfo("EOS_8_4", "EOS4A16", 4, 8, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1145
    ChInfo("EOS_1_-4", "EOS4C02", -4, 1, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1146
    ChInfo("EOS_2_-4", "EOS4C04", -4, 2, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1147
    ChInfo("EOS_3_-4", "EOS4C06", -4, 3, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1148
    ChInfo("EOS_4_-4", "EOS4C08", -4, 4, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1149
    ChInfo("EOS_5_-4", "EOS4C10", -4, 5, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1150
    ChInfo("EOS_6_-4", "EOS4C12", -4, 6, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1151
    ChInfo("EOS_7_-4", "EOS4C14", -4, 7, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1152
    ChInfo("EOS_8_-4", "EOS4C16", -4, 8, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1153
    ChInfo("EOS_1_5", "EOS5A02", 5, 1, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1154
    ChInfo("EOS_2_5", "EOS5A04", 5, 2, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1155
    ChInfo("EOS_3_5", "EOS5A06", 5, 3, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1156
    ChInfo("EOS_4_5", "EOS5A08", 5, 4, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1157
    ChInfo("EOS_5_5", "EOS5A10", 5, 5, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1158
    ChInfo("EOS_6_5", "EOS5A12", 5, 6, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1159
    ChInfo("EOS_7_5", "EOS5A14", 5, 7, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1160
    ChInfo("EOS_8_5", "EOS5A16", 5, 8, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1161
    ChInfo("EOS_1_-5", "EOS5C02", -5, 1, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1162
    ChInfo("EOS_2_-5", "EOS5C04", -5, 2, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1163
    ChInfo("EOS_3_-5", "EOS5C06", -5, 3, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1164
    ChInfo("EOS_4_-5", "EOS5C08", -5, 4, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1165
    ChInfo("EOS_5_-5", "EOS5C10", -5, 5, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1166
    ChInfo("EOS_6_-5", "EOS5C12", -5, 6, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1167
    ChInfo("EOS_7_-5", "EOS5C14", -5, 7, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1168
    ChInfo("EOS_8_-5", "EOS5C16", -5, 8, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1169
    ChInfo("EOS_1_6", "EOS6A02", 6, 1, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1170
    ChInfo("EOS_2_6", "EOS6A04", 6, 2, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1171
    ChInfo("EOS_3_6", "EOS6A06", 6, 3, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1172
    ChInfo("EOS_4_6", "EOS6A08", 6, 4, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1173
    ChInfo("EOS_5_6", "EOS6A10", 6, 5, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1174
    ChInfo("EOS_6_6", "EOS6A12", 6, 6, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1175
    ChInfo("EOS_7_6", "EOS6A14", 6, 7, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1176
    ChInfo("EOS_8_6", "EOS6A16", 6, 8, "EOS", 2, 3, 48, 3, 48, 12, 1, 1, 2, 1),  # 1177
    ChInfo("EOS_1_-6", "EOS6C02", -6, 1, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1178
    ChInfo("EOS_2_-6", "EOS6C04", -6, 2, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1179
    ChInfo("EOS_3_-6", "EOS6C06", -6, 3, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1180
    ChInfo("EOS_4_-6", "EOS6C08", -6, 4, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1181
    ChInfo("EOS_5_-6", "EOS6C10", -6, 5, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1182
    ChInfo("EOS_6_-6", "EOS6C12", -6, 6, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1183
    ChInfo("EOS_7_-6", "EOS6C14", -6, 7, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1184
    ChInfo("EOS_8_-6", "EOS6C16", -6, 8, "EOS", 2, 3, 48, 3, 48, 12, 2, 2, 1, 1),  # 1185
    # BMS cutout BOS6-projective, BOG-rail, EMS1/3, !!!
]
MAXCHAMBERS = len(mdt)

# List of chambers with cutouts
cutout_chambers = ['BIR1A11', 'BIR1A15', 'BMS4C02', 'BMS4C04', 'BMS4C06', 'BMS4C08', 'BMS4C10', 'BMS4C16', 'BMS6C02',
                   'BMS6C04', 'BMS6C06', 'BMS6C08', 'BMS6C10', 'BMS6C16', 'BMG2A12', 'BMG2A14', 'BMG2C12', 'BMG2C14',
                   'BMG4A12', 'BMG4A14', 'BMG4C12', 'BMG4C14', 'BMG6A12', 'BMG6A14', 'BMG6C12', 'BMG6C14']

# Channel Mapping
# for all 3x8 chambers
mapI = [6, 1, 8, 2, 7, 3, 5, 4]  # HH Type 1	map3x8b
mapII = [8, 1, 7, 2, 6, 3, 5, 4]  # HH Type 2	map3x8a

# for 4x6 EndCap chambers (EIS,EIL in H8)
mapIII = [5, 6, 4, 2, 3, 1]  # Type 3    map436
mapIV = [4, 2, 5, 1, 6, 3]  # Type 4    map446
map4x6 = [4, 1, 5, 2, 6, 3]  # special   map4x6

map4x6g = [2, 1, 3, 5, 4, 6]  # Type 5 BIM #1,3 on EIL4 for III
map4x6h = [3, 5, 2, 6, 1, 4]  # Type 6 BIM #0,2 on EIL4 for IV
# for 4x6 barrel chambers (BIL1,BIL2 in H8)
map4x6d = [1, 3, 2, 4, 6, 5]  #
map4x6e = [3, 6, 1, 5, 2, 4]  #
map4x6f = [3, 6, 2, 5, 1, 4]  #

#  mezzchannelmap is a map of mezzcard channels for all 4 mezzcard types.
#  It maps mezzcard type,layer,tube to mezzcard channel as follows:
#  mezzcard channel = mezzchannelmap[type][layer][tube]
#  where type=1..4, layer=1..4, tube=1..8
#  -1's are used for the 0 indices so that the type,layer, tube numbering
#  starts at 1 rather than 0 to match the hardware numbering conventions.
#  Also -1's are inserted to make all tube indices go to 8, to prevent
#  accidental array out of bounds.
#  However, -1 indicates that the type,layer,tube combination is invalid
#  Implement as tuple for immutability and speed.

# ORIGINAL
mezzchannelmap = (
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1),
     (-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 3, 5, 7, 6, 0, 4, 2), (-1, 9, 11, 13, 15, 14, 8, 12, 10),
     (-1, 17, 19, 21, 23, 22, 16, 20, 18), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 3, 5, 7, 6, 4, 2, 0), (-1, 9, 11, 13, 15, 14, 12, 10, 8),
     (-1, 17, 19, 21, 23, 22, 20, 18, 16), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 5, 3, 4, 2, 0, 1, -1, -1), (-1, 11, 9, 10, 8, 6, 7, -1, -1),
     (-1, 17, 15, 16, 14, 12, 13, -1, -1), (-1, 23, 21, 22, 20, 18, 19, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 3, 1, 5, 0, 2, 4, -1, -1), (-1, 9, 7, 11, 6, 8, 10, -1, -1),
     (-1, 15, 13, 17, 12, 14, 16, -1, -1), (-1, 19, 21, 23, 18, 20, 22, -1, -1))
)

#  Map for BA side chambers.
mezzchannelmapBA = (
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1),
     (-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 3, 5, 7, 6, 0, 4, 2), (-1, 9, 11, 13, 15, 14, 8, 12, 10),
     (-1, 17, 19, 21, 23, 22, 16, 20, 18), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 3, 5, 7, 6, 4, 2, 0), (-1, 9, 11, 13, 15, 14, 12, 10, 8),
     (-1, 17, 19, 21, 23, 22, 20, 18, 16), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 0, 2, 4, 3, 5, -1, -1), (-1, 7, 6, 8, 10, 9, 11, -1, -1),
     (-1, 13, 12, 14, 16, 15, 17, -1, -1), (-1, 19, 18, 20, 22, 21, 23, -1, -1)),  # changed
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 4, 2, 0, 5, 1, 3, -1, -1), (-1, 10, 8, 6, 11, 7, 9, -1, -1),
     (-1, 16, 14, 12, 17, 13, 15, -1, -1), (-1, 22, 20, 18, 23, 21, 19, -1, -1))  # changed
)
#  Map for BC side chambers.
mezzchannelmapBC = (
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1),
     (-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 3, 5, 7, 6, 0, 4, 2), (-1, 9, 11, 13, 15, 14, 8, 12, 10),
     (-1, 17, 19, 21, 23, 22, 16, 20, 18), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 3, 5, 7, 6, 4, 2, 0), (-1, 9, 11, 13, 15, 14, 12, 10, 8),
     (-1, 17, 19, 21, 23, 22, 20, 18, 16), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 19, 18, 20, 22, 21, 23, -1, -1), (-1, 13, 12, 14, 16, 15, 17, -1, -1),
     (-1, 7, 6, 8, 10, 9, 11, -1, -1), (-1, 1, 0, 2, 4, 3, 5, -1, -1)),  # changed
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 22, 20, 18, 23, 21, 19, -1, -1), (-1, 16, 14, 12, 17, 13, 15, -1, -1),
     (-1, 10, 8, 6, 11, 7, 9, -1, -1), (-1, 4, 2, 0, 5, 1, 3, -1, -1))  # changed
)
# BEE1A,
mezzchannelmapEA = (
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1),
     (-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 3, 5, 7, 6, 0, 4, 2), (-1, 9, 11, 13, 15, 14, 8, 12, 10),
     (-1, 17, 19, 21, 23, 22, 16, 20, 18), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 3, 5, 7, 6, 4, 2, 0), (-1, 9, 11, 13, 15, 14, 12, 10, 8),
     (-1, 17, 19, 21, 23, 22, 20, 18, 16), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 5, 3, 4, 2, 0, 1, -1, -1), (-1, 11, 9, 10, 8, 6, 7, -1, -1),
     (-1, 17, 15, 16, 14, 12, 13, -1, -1), (-1, 23, 21, 22, 20, 18, 19, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 3, 1, 5, 0, 2, 4, -1, -1), (-1, 9, 7, 11, 6, 8, 10, -1, -1),
     (-1, 15, 13, 17, 12, 14, 16, -1, -1), (-1, 19, 21, 23, 18, 20, 22, -1, -1))
)
#  Map for C side chambers.
mezzchannelmapEC = (
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1),
     (-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 3, 5, 7, 6, 0, 4, 2), (-1, 9, 11, 13, 15, 14, 8, 12, 10),
     (-1, 17, 19, 21, 23, 22, 16, 20, 18), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 3, 5, 7, 6, 4, 2, 0), (-1, 9, 11, 13, 15, 14, 12, 10, 8),
     (-1, 17, 19, 21, 23, 22, 20, 18, 16), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 23, 21, 22, 20, 18, 19, -1, -1), (-1, 17, 15, 16, 14, 12, 13, -1, -1),
     (-1, 11, 9, 10, 8, 6, 7, -1, -1), (-1, 5, 3, 4, 2, 0, 1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 19, 21, 23, 18, 20, 22, -1, -1), (-1, 15, 13, 17, 12, 14, 16, -1, -1),
     (-1, 9, 7, 11, 6, 8, 10, -1, -1), (-1, 3, 1, 5, 0, 2, 4, -1, -1))
)

mezzchannelmapBIR3 = (
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1),
     (-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 3, 5, 7, 6, 0, 4, 2), (-1, 9, 11, 13, 15, 14, 8, 12, 10),
     (-1, 17, 19, 21, 23, 22, 16, 20, 18), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 1, 3, 5, 7, 6, 4, 2, 0), (-1, 9, 11, 13, 15, 14, 12, 10, 8),
     (-1, 17, 19, 21, 23, 22, 20, 18, 16), (-1, -1, -1, -1, -1, -1, -1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 22, 21, 23, 20, 18, 19, -1, -1), (-1, 16, 15, 17, 14, 12, 13, -1, -1),
     (-1, 10, 9, 11, 8, 6, 7, -1, -1), (-1, 4, 3, 5, 2, 0, 1, -1, -1)),
    ((-1, -1, -1, -1, -1, -1, -1, -1, -1), (-1, 23, 21, 19, 18, 20, 22, -1, -1), (-1, 17, 13, 15, 12, 14, 16, -1, -1),
     (-1, 11, 7, 9, 6, 8, 10, -1, -1), (-1, 5, 1, 3, 0, 2, 4, -1, -1))
)

#  Number of tubes per layer in mezzcard
mezzcardtubes = (-1, 8, 8, 6, 6)


#  Check for valid chamber name.
#  Returns mdt[] index of chamber, else -1
def CheckChamber(chamber, ml, layer, tube):
    for ii in range(0, MAXCHAMBERS):
        if (chamber == mdt[ii].hardname or chamber == mdt[ii].calname) and \
                layer > 0 and tube > 0 and \
                ((ml == 1 and layer <= mdt[ii].nly_ml1 and tube <= mdt[ii].ntl_ml1) or \
                 (ml == 2 and layer <= mdt[ii].nly_ml2 and tube <= mdt[ii].ntl_ml2)):
            return ii;
    return -1


#  Returns index in mdt[] for ChName
def MDTindex(ChName):
    if type(ChName) is int:  # assume to be an index or muonfixedid if int
        #  If looks like an chamber index already, just return
        if ChName > 0 and ChName < MAXCHAMBERS:
            return ChName
        #  Else treat as muonfixedid
        else:
            ChName = '%s_%i_%i' % (
            muonfixedid.stationNameString(ChName), muonfixedid.stationPhi(ChName), muonfixedid.stationEta(ChName))
        #      return MDTcheckMfid(ChName)
    return CheckChamber(ChName, 1, 1, 1)


#  Returns muonfixedid for ChName
def MDTmfid(ChName, ml=1, ly=1, tb=1):
    # if ml > 1000 assume it is an MLLT
    if ml > 1000:
        mllt = ml
        ml = mllt / 1000
        ly = (mllt - ml * 1000) / 100
        tb = mllt - ml * 1000 - ly * 100
    # Check that ChName, ml,ly,tb are valid
    idx = CheckChamber(ChName, ml, ly, tb)
    if idx == -1: return -1
    return muonfixedid.ID(mdt[idx].station, mdt[idx].phi, mdt[idx].eta, ml, ly, tb)


#  Checks muonfixedid: Returns MDTindex if mfid is valid; -1 if not
def MDTcheckMfid(mfid):
    ChName = '%s_%i_%i' % (
    muonfixedid.stationNameString(mfid), muonfixedid.stationPhi(mfid), muonfixedid.stationEta(mfid))
    ml = muonfixedid.mdtMultilayer(mfid)
    ly = muonfixedid.mdtTubeLayer(mfid)
    tb = muonfixedid.mdtTube(mfid)
    # Check that ChName, ml,ly,tb are valid
    return CheckChamber(ChName, ml, ly, tb)


# Returns hardware name from idx (which can be actual mdt[] index, calname or muonfixedid)
# Cannot overload functions so allow argument to be int (idx) or string (calibname)
def MDThardname(idx):
    if type(idx) is int:
        if idx < 0:
            return "IsWRONG"
        elif idx >= MAXCHAMBERS:  # assume it is a muonfixedid
            idx = MDTcheckMfid(idx)
    else:  # Assume is a hardname or calname
        idx = MDTindex(idx)
    if idx == -1: return "IsWRONG"
    return mdt[idx].hardname


# Returns calname from idx (which can be actual mdt[] index, hardname or muonfixedid)
def MDTcalname(idx):
    if type(idx) is int:
        if idx < 0:
            return "IsWRONG"
        elif idx >= MAXCHAMBERS:  # assume it is a muonfixedid
            idx = MDTcheckMfid(idx)
    else:  # Assume is a hardname or calname
        idx = MDTindex(idx)
    if idx == -1: return "IsWRONG"
    return mdt[idx].calname


# Returns hardware name-ML-L-T from a muonfixedid
def MDTtubename(id):
    idx = MDTindex(
        '%s_%i_%i' % (muonfixedid.stationNameString(id), muonfixedid.stationPhi(id), muonfixedid.stationEta(id)))
    if idx == -1: return 'UnknownMFID %i' % id
    return '%s-%i-%i-%i' % (
    mdt[idx].hardname, muonfixedid.mdtMultilayer(id), muonfixedid.mdtTubeLayer(id), muonfixedid.mdtTube(id))


# Returns #ML in the chamber
def MDTnML(ChName):
    idx = MDTindex(ChName)
    if idx < 0: return -1
    return mdt[idx].num_ml


# Returns TOT #Layers in the chamber
def MDTtotalLayers(ChName):
    idx = MDTindex(ChName)
    if idx < 0: return -1
    return MDTnLml(ChName, 0)


# Returns TOT #Tubes  in the chamber
def MDTtotalTubes(ChName):
    idx = MDTindex(ChName)
    if idx < 0: return -1
    return MDTnTml(ChName, 0)


# Returns #Mezzanines in the chamber
def MDTnmezz(ChName):
    idx = MDTindex(ChName)
    if idx < 0: return -1
    return mdt[idx].n_mezz


# Returns number of mezzcards included skipped mezzcards due to cut outs
def MDTmaxmezz(ChName):
    idx = MDTindex(ChName)
    if idx < 0: return -1
    icutout = 0
    hardname = mdt[idx].hardname
    # Only cutouts in BI and BM
    if hardname[0:2] == 'BI' or hardname[0:2] == 'BM':
        for chamber in cutout_chambers:
            #  These are the chambers with cutouts
            if hardname == chamber:
                icutout = 1
                break
    return mdt[idx].n_mezz + icutout


# Returns the ML MEZZ type (1-4)
def MDTtypeML(ChName, ml):
    if ml != 1 and ml != 2:
        print("MDTtypeML bad ml=%i. Returned 0" % (ml))
        return 0
    idx = MDTindex(ChName)
    if idx < 0:
        return -1
    elif ml == 1:
        idx = mdt[idx].mzt_ml1
    elif ml == 2:
        idx = mdt[idx].mzt_ml2
    return idx


# Returns the MZ MEZZ type (1-4)
def MDTtypeMZ(ChName, mz):
    ml = MDTmlMZ(ChName, mz)
    return MDTtypeML(ChName, ml)


# Returns #ML where there is Mezz#0
def MDTmlMZ0(ChName):
    idx = MDTindex(ChName)
    if idx < 0: return -1
    return mdt[idx].mz0ml


# Returns #ML of Mezz# mz
def MDTmlMZ(ChName, mz):
    m0m = MDTmlMZ0(ChName)
    if m0m == 0: return -1
    if mz % 2 == 0: return m0m
    return 3 - m0m


# Returns #Layer in the ML
def MDTnLml(ChName, ml):
    if ml < 0 or ml > 2:
        print("MDTnLml bad ml=%i. Returned 0\n" % (ml))
        return -1
    nl_ml = 0
    idx = MDTindex(ChName);
    if idx >= 0:
        if ml == 1:
            nl_ml = mdt[idx].nly_ml1
        elif ml == 2:
            nl_ml = mdt[idx].nly_ml2
        elif ml == 0:
            nl_ml = self, mdt[idx].nly_ml1 + mdt[idx].nly_ml2
    return nl_ml


# Returns #Tubes/layer in the ML
def MDTnTly(ChName, ml):
    if ml < 0 or ml > 2:
        print("MDTnTly bad ml=%i. Returned -1" % (ml))
        return -1
    nt_ly = 0
    idx = MDTindex(ChName)
    if idx >= 0:
        if ml == 1:
            nt_ly = mdt[idx].ntl_ml1
        elif ml == 2:
            nt_ly = mdt[idx].ntl_ml2
        elif ml == 0:
            nt_ly = mdt[idx].ntl_ml1 + mdt[idx].ntl_ml2
    return nt_ly


# Returns #Tubes in the ML
def MDTnTml(ChName, ml):
    if ml < 0 or ml > 2:
        print("MDTnTml bad ml=%i. Returned -1\n" % (ml))
        return -1
    nt_ml = 0
    idx = MDTindex(ChName)
    if idx >= 0:
        if ml == 1:
            nt_ml = mdt[idx].ntl_ml1 * mdt[idx].nly_ml1
        elif ml == 2:
            nt_ml = mdt[idx].ntl_ml2 * mdt[idx].nly_ml2
        elif ml == 0:
            nt_ml = mdt[idx].ntl_ml1 * mdt[idx].nly_ml1 + \
                    mdt[idx].ntl_ml2 * mdt[idx].nly_ml2
    return nt_ml


# Convert MLLT to ml, ly, tb; Returns tuple ml, ly, tb
def MLLT2MLLT(ChName, mllt):
    OK = 1
    ml = mllt / 1000
    ly = (mllt / 100) % 10
    nt = mllt % 100
    if mllt <= 0 or mllt > 2478:
        OK = 0
    elif ml < 1 or ml > 2:
        OK = 0
    elif ly < 1 or ly > MDTnLml(ChName, ml):
        OK = 0
    elif nt < 1 or nt > MDTnTly(ChName, ml):
        OK = 0
    if OK == 0:
        ml = -1
        ly = -1
        nt = -1
    return ml, ly, nt


# Convert tubenum [1..] to MLLT
def T2MLLT(ChName, tb):
    idx = MDTindex(ChName)
    if idx < 0 or tb < 0 or tb > MDTtotalTubes(ChName):
        print(' T2MLLT %s tb=%i tube number out of range' % (ChName, tb))
        return 0

    ml = 1
    if tb > MDTnTml(ChName, 1):
        ml = 2
        tb -= MDTnTml(ChName, 1)  # now tubenum in ML2

    ly = 1 + tb / MDTnTly(ChName, ml)
    if tb % MDTnTly(ChName, ml) == 0: ly -= 1

    nt = tb - (ly - 1) * MDTnTly(ChName, ml)  # now tubenum in that layer
    mllt = ml * 1000 + ly * 100 + nt
    # Test if valid mllt
    xml, xly, xnt = MLLT2MLLT(ChName, mllt);
    if xml == -1: mllt = 0;
    return mllt;


# Convert MLLT to tubenum
def MLLT2T(ChName, mllt):
    ml, ly, nt = MLLT2MLLT(ChName, mllt)
    if ml == -1: return -1
    return (ml - 1) * MDTnTml(ChName, 1) + (ly - 1) * MDTnTly(ChName, ml) + nt


# MLLT to layer [1..] note this is total number of layers, not layer within ML
def MLLT2L(ChName, mllt):
    ml, ly, nt = MLLT2MLLT(ChName, mllt)
    if ml == -1: return -1
    return (ml - 1) * MDTnLml(ChName, 1) + ly


# MLLT  to mezzNumber
def MLLT2M(ChName, mllt):
    imezz = -1
    ml, ly, nt = MLLT2MLLT(ChName, mllt)
    if ml != -1:
        ntl_mez = 24 / MDTnLml(ChName, ml)
        imezz = MDTnML(ChName) * ((nt - 1) / ntl_mez)
        if ml != MDTmlMZ0(ChName): imezz = imezz + 1
    return imezz


# Tube number  to mezzNumber
def T2M(ChName, tb):
    mllt = T2MLLT(ChName, tb)
    return MLLT2M(ChName, mllt)


#  Find mezzcard type, mezzcard channel for chamber, mllt combination.
#  cham = Hardware/software name, mdt[] index, or muonfixedid.
#  If muonfixedid is used, it is use to determine the mllt.
#  returns a ntuple of (mezzcard type, mezzcard channel)
#  returns (-1,-1) if error occurs.
#  Note that mezzcard types are 1..4
#            mezzcard channels are 0..23
def MLLT2MezzCh(cham, mllt=0):
    mfid = 0
    # Code taken from MDThardname
    if type(cham) is int:
        if cham < 0:
            print("MLLT2MezzCh: bad cham", cham)
            return -1, -1
        elif cham >= MAXCHAMBERS:  # assume it is a muonfixedid
            mfid = cham
            idx = MDTindex('%s_%i_%i' % (
            muonfixedid.stationNameString(mfid), muonfixedid.stationPhi(mfid), muonfixedid.stationEta(mfid)))
        else:  # assume is already a chamber index
            idx = cham
    else:  # Assume is a hardname or calname
        idx = MDTindex(cham)

    #  Check for invalid chamber
    if idx == -1:
        print('MLLT2MezzCh ERROR: Bad chamber', cham)
        return -1, -1

    ChName = mdt[idx].hardname

    #  if muonfixedid has been passed get ml,ly,tb from muonfixedid
    #  otherwise get it from mllt
    if mfid == 0:
        (ml, ly, tb) = MLLT2MLLT(ChName, mllt)
    else:
        ml = muonfixedid.mdtMultilayer(mfid)
        ly = muonfixedid.mdtTubeLayer(mfid)
        tb = muonfixedid.mdtTube(mfid)

    # Check for valid ml,ly,tb
    if ml < 1 or ml > 2 \
            or ly < 1 or ly > MDTnLml(ChName, ml) \
            or tb < 1 or tb > MDTnTly(ChName, ml):
        # This print just finds the odd chambers like BMS4, BMS6, BIR
        # which have different number of tubes on each ML
        # Database contains these fantom tubes
        #    print 'MLLT2MezzCh ERROR: Bad chamber or mllt',ChName,mllt
        return -1, -1
    # Get mezzcard type.  Actually there are mezzcard types 5,6 which are ignored now.
    mezztype = MDTtypeML(ChName, ml)
    if mezztype < 1 or mezztype > 4:
        #    print 'MLLT2MezzCh ERROR: Bad mezztype',ChName,mllt,mezztype
        return -1, -1

    # tbi = tube index within a mezzcard
    tbi = tb % mezzcardtubes[mezztype]
    if tbi == 0: tbi = mezzcardtubes[mezztype]

    mezzchan = -2
    # A/C sides are mirror images, use different maps
    station = ChName[0:3]
    LS = ChName[2]  # Could be L,S,E,M,R,F,G
    side = ChName[4]
    if ChName[0] == 'E' or ChName[1] == 'E':  # Endcap + BEE
        if side == 'A':
            mezzchan = mezzchannelmapEA[mezztype][ly][tbi]
        else:
            mezzchan = mezzchannelmapEC[mezztype][ly][tbi]
    else:  # Barrel
        # BIM1A11 uses C map     BIMxA11 use C map
        if station == 'BIM' or station == 'BIR':
            #      if station == 'BIR' and int(ChName[3]) > 2:
            #        if side == 'A': mezzchan = mezzchannelmapBIR3[mezztype][ly][tbi]
            #        else:           mezzchan = mezzchannelmapEA[mezztype][ly][tbi]

            if ChName[5:7] == '11':  # BIMxx11, BIRxx11
                if side == 'A':
                    mezzchan = mezzchannelmapBC[mezztype][ly][tbi]
                else:
                    mezzchan = mezzchannelmapBA[mezztype][ly][tbi]
            elif side == 'A':
                mezzchan = mezzchannelmapBA[mezztype][ly][tbi]
            else:
                mezzchan = mezzchannelmapBC[mezztype][ly][tbi]

        # BISxx12
        elif station == 'BIS' and ChName[5:7] == '12':
            if side == 'A':
                mezzchan = mezzchannelmapEC[mezztype][ly][tbi]
            else:
                mezzchan = mezzchannelmapEA[mezztype][ly][tbi]
        elif LS == 'S':
            if side == 'A':
                mezzchan = mezzchannelmapEA[mezztype][ly][tbi]
            else:
                mezzchan = mezzchannelmapEC[mezztype][ly][tbi]
        else:
            if side == 'A':
                mezzchan = mezzchannelmapBA[mezztype][ly][tbi]
            else:
                mezzchan = mezzchannelmapBC[mezztype][ly][tbi]
    return mezztype, mezzchan


########################################################################
#  Convert date in DD-<Month>-YYYY to YYYYMMDD
#  where <Month> = Jan, Feb, etc
########################################################################
def getdate(date):
    date2 = '0'
    #  If do not find date give up
    if date == '':  # return ''
        print('getdate ERROR: no date found for', headID)
        return '0 0'

    # convert date to YYYYMMDD
    months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for imon in range(1, 12):
        if date[3:6] == months[imon]:
            date2 = date[7:] + '%2.2i' % imon + date[:2]
            break

    #  Return date and run number
    return date2


# Calculate #TubeIndex in the ML
def MDTtubeIndex(ChName, ml, ly, tube):
    if ml < 1 or ml > 2:
        print("MDTnTml bad ml=%i. Returned -1\n" % (ml))
        return -1
    tubeIndex = 0
    idx = MDTindex(ChName)
    if idx >= 0:
        tubeIndex = (ml - 1) * mdt[idx].ntl_ml1 * mdt[idx].nly_ml1 + \
                    (ly - 1) * mdt[idx].ntl_ml1 + tube - 1
    return tubeIndex


# Calculate MLLT from #TubeIndex
def MDTtubeIndex2MLLT(ChName, tubeIndex):
    idx = MDTindex(ChName)
    ml = tubeIndex / (mdt[idx].ntl_ml1 * mdt[idx].nly_ml1) + 1
    ly = tubeIndex / mdt[idx].ntl_ml1 + 1 - (ml - 1) * mdt[idx].nly_ml1
    tb = tubeIndex % mdt[idx].ntl_ml1 + 1
    print(tubeIndex, mdt[idx].ntl_ml1, mdt[idx].nly_ml1, ml, ly, tb, MDTtubeIndex(ChName, ml, ly, tb))
    return ml * 1000 + ly * 100 + tb


# Calculate ASD Index from muonfixedid
def MDTasdIndex(id):
    icham = MDTindex(id)
    chName = MDThardname(icham)
    ml = muonfixedid.mdtMultilayer(id)
    ly = muonfixedid.mdtTubeLayer(id)
    tb = muonfixedid.mdtTube(id)
    nMezz = MLLT2M(chName, ml * 1000 + ly * 100 + tb)
    mezzType, nMezzCh = MLLT2MezzCh(chName, ml * 1000 + ly * 100 + tb)
    nASD = 0
    if nMezzCh in range(8):
        nASD = 1
    elif nMezzCh in range(8, 16):
        nASD = 2
    elif nMezzCh in range(16, 24):
        nASD = 3
    # if nASD == 0 :
    #  print 'error Mezz channel',chName, ml,ly,tb, nMezz,nMezzCh
    asdChannel = icham * 1000 + nMezz * 10 + nASD
    return asdChannel


########################################################################
### This is for testing porpoises
########################################################################
def main(argv):
    cham = ''
    mllt = 0
    try:
        cham = int(argv[0])
    except:
        cham = argv[0]
        mllt = int(argv[1])
    (mezztype, mezzchan) = MLLT2MezzCh(cham, mllt)
    print('Results', cham, mllt, mezztype, mezzchan)
    return
    print(mdt[0].calname, mdt[1].hardname)
    print("BEE1A04", MDTindex("BEE1A04"))
    print("EOS6C14", MDTindex("EOS6C14"))
    print("EOS6C14-1-1-1", CheckChamber("EOS6C14", 1, 1, 1))
    print("EOS6C14-1-1-89", CheckChamber("EOS6C14", 1, 1, 89))
    chamber = "EEL1C13"
    mllt = 1208
    for i in range(0, 8):
        print(chamber, mllt, MLLT2MLLT(chamber, mllt), MLLT2M(chamber, mllt))
        mllt = mllt + 8
    print(MDThardname(34), MDThardname("BIL_1_1"))


if __name__ == "__main__":
    main(sys.argv[1:])

