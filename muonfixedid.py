# module based on MuonIdUnpack.py
#  unpack numberic MuonId and convert to station Phi phi etc.

#  Get MuonfixedID from chamber parameters
def ID(station, phi, eta, ml=1, ly=1, tb=1):
    mfid = -1
    if type(station) is str:
        loc_station = __kStationNameStringsMap[station] + 1
        loc_station -= __kStationNameMin
        loc_station &= __kStationNameMask
        loc_eta = (eta - __kStationEtaMin) & __kStationEtaMask
        loc_phi = (phi - __kStationPhiMin) & __kStationPhiMask
        loc_ml = (ml - __kMdtMultilayerMin) & __kMdtMultilayerMask
        loc_ly = (ly - __kMdtTubeLayerMin) & __kMdtTubeLayerMask
        loc_tb = (tb - __kMdtTubeMin) & __kMdtTubeMask
        mfid = (loc_station << __kStationNameShift) | (loc_eta << __kStationEtaShift) | (
                    loc_phi << __kStationPhiShift) | (loc_ml << __kMdtMultilayerShift) | (
                           loc_ly << __kMdtTubeLayerShift) | (loc_tb << __kMdtTubeShift) | __kUnusedBits
    return mfid


# station name
def stationNameIndex(mfid):
    if type(mfid) is int:
        return (mfid >> __kStationNameShift) & __kStationNameMask
    return -1


def stationName(mfid):
    if type(mfid) is int:
        return stationNameIndex(mfid) + __kStationNameMin
    return -1


def stationNameString(mfid):
    if type(mfid) is int:
        return __kStationNameStrings[stationName(mfid) - 1]
    return 'ERROR'


# station Phi
def stationPhiIndex(mfid):
    if type(mfid) is int:
        return (mfid >> __kStationPhiShift) & __kStationPhiMask
    return -1


def stationPhi(mfid):
    if type(mfid) is int:
        return stationPhiIndex(mfid) + __kStationPhiMin
    return -1


# station Eta
def stationEtaIndex(mfid):
    if type(mfid) is int:
        return (mfid >> __kStationEtaShift) & __kStationEtaMask
    return -1  # hmm, -1 is a valid eta index


def stationEta(mfid):
    if type(mfid) is int:
        return stationEtaIndex(mfid) + __kStationEtaMin
    return -1


# multilayer
def mdtMultilayerIndex(mfid):
    if type(mfid) is int:
        return (mfid >> __kMdtMultilayerShift) & __kMdtMultilayerMask
    return -1


def mdtMultilayer(mfid):
    if type(mfid) is int:
        return mdtMultilayerIndex(mfid) + __kMdtMultilayerMin
    return -1


# TubeLayer (helper function)
def mdtTubeLayerIndex(mfid):
    if type(mfid) is int:
        return (mfid >> __kMdtTubeLayerShift) & __kMdtTubeLayerMask
    return -1


# Tube layer within ML.  Counting from 1
def mdtTubeLayer(mfid):
    if type(mfid) is int:
        return mdtTubeLayerIndex(mfid) + __kMdtTubeLayerMin
    return -1


# TubeNumber (helper function)
def mdtTubeIndex(mfid):
    if type(mfid) is int:
        return (mfid >> __kMdtTubeShift) & __kMdtTubeMask
    return -1


# Tube number within layer.  Counting from 1
def mdtTube(mfid):
    if type(mfid) is int:
        return mdtTubeIndex(mfid) + __kMdtTubeMin
    return -1


# Decode Tech ID
# return type of technology: values: 0=MDT 1=CSC 2=TGC 3=RPC -1=Not valid
def TechID(mfid):
    if type(mfid) is int:
        techid = ((mfid >> __kTechnologyShift) & __kTechnologyMask) + __kTechnologyMin
        if techid >= 0 and techid <= 3: return techid
    return -1


# return name of technology: values: MDT CSC TGC RPC UNK (UNK=unknown)
def cTechID(mfid):
    techname = ['MDT', 'CSC', 'TGC', 'RPC']
    techid = ((mfid >> __kTechnologyShift) & __kTechnologyMask) + __kTechnologyMin
    if techid >= 0 and techid <= 3:
        return techname[techid]
    return 'UNK'


# Write character string for track author in calib ntuple
def track_author(iauthor):
    if iauthor == 0:
        return 'Moore'
    elif iauthor == 1:
        return 'BckExSAnoCal'  # BackExtrapolated SA track with MuonTrackThroughCalo without calorimeter energy correction
    elif iauthor == 2:
        return 'BckExSAwCal'  # BackExtrapolated SA track with MuonTrackThroughCalo with calorimeter energy correction
    elif iauthor == 10:
        return 'MuidSAExIP'  # MuidSA/ExtrapolateToIP (Moore track to vertex and refitted)
    elif iauthor == 20:
        return 'MuidCBComMu'  # MuidCB/CombinedMuon (combined inner detector - muon spectrometer track)
    elif iauthor == 25:
        return 'MuonCombinedFit'
    elif iauthor == 30:
        return 'MuTagIMO'
    elif iauthor == 35:
        return 'MuidMuGirl'
    elif iauthor == 40:
        return 'AODMuidCB'  # AOD MuidCB/CombinedMuon
    elif iauthor == 41:
        return 'AODMuidSAExIP'  # MuidSA/ExtrapolateToIP
    elif iauthor == 42:
        return 'AODMuTagIMO'
    elif iauthor == 43:
        return 'AODMuGirl'
    elif iauthor == 100:
        return 'Muonboy'
    elif iauthor == 120:
        return 'Staco'
    elif iauthor == 130:
        return 'MuTag'
    elif iauthor == 140:
        return 'AODStacoMuonCB'
    elif iauthor == 141:
        return 'AODStacoMuonSA'
    elif iauthor == 142:
        return 'AODStacoMuonTag'
    elif iauthor == 1000:
        return 'IDtrack'  # Inner Detector track
    return 'unknown_%i' % iauthor


# Write character string for track hit type in calib ntuple
def track_hittype(itype):
    if itype == -2:
        return 'RIOcompetingRIO'  # RIO contained in the competing RIO
    elif itype == 1:
        return 'HitOnTrack'
    elif itype == 2:
        return 'CompeteTGCRPC'  # Competing RIO used for TGC and RPC
    elif itype == 3:
        return 'PseudoHit'  # Pseudo measurement (needed to stabilize the fit)
    elif itype == 4:
        return 'Outlier'
    elif itype == 5:
        return 'DeltaRay'
    elif itype == 6:
        return 'Hole'
    elif itype == 11:
        return 'PhiScatCenter'  # Scattering centre in phi
    elif itype == 12:
        return 'ThetaScatCenter'  # Scattering centre in theta
    return 'unknown_%i' % itype


__kTechnologyMask = 3
__kTechnologyShift = 30
__kTechnologyMin = 0

__kMdtMultilayerMask = 1
__kMdtMultilayerShift = 9
__kMdtMultilayerMin = 1

__kMdtTubeLayerMask = 3
__kMdtTubeLayerShift = 7
__kMdtTubeLayerMin = 1

__kMdtTubeMask = 127
__kMdtTubeShift = 0
__kMdtTubeMin = 1

__kStationNameMask = 63
__kStationNameShift = 24
__kStationNameMin = 1

__kStationEtaMask = 31
__kStationEtaShift = 19
__kStationEtaMin = -8

__kStationPhiMask = 63
__kStationPhiShift = 13
__kStationPhiMin = 1

# Unused bits 11-13 which are set to 111 in muonfixedid for MDTs
__kUnusedBits = 7168

__kStationNameStrings = ['BIL', 'BIS', 'BML', 'BMS', 'BOL', 'BOS', 'BEE', 'BIR', 'BMF', 'BOF', 'BOG', 'BME', 'BIM',
                         'EIC', 'EIL', 'EEL', 'EES', 'EMC', 'EML', 'EMS', 'EOC', 'EOL', 'EOS', 'EIS',
                         'T1F', 'T1E', 'T2F', 'T2E', 'T3F', 'T3E', 'T4F', 'T4E', 'CSS', 'CSL', 'BMG']

__kStationNameStringsMap = {'BIL': 0, 'BIS': 1, 'BML': 2, 'BMS': 3, 'BOL': 4, 'BOS': 5, 'BEE': 6, 'BIR': 7, 'BMF': 8,
                            'BOF': 9, 'BOG': 10, 'BME': 11, 'BIM': 12,
                            'EIC': 13, 'EIL': 14, 'EEL': 15, 'EES': 16, 'EMC': 17, 'EML': 18, 'EMS': 19, 'EOC': 20,
                            'EOL': 21, 'EOS': 22, 'EIS': 23,
                            'T1F': 24, 'T1E': 25, 'T2F': 26, 'T2E': 27, 'T3F': 28, 'T3E': 29, 'T4F': 30, 'T4E': 31,
                            'CSS': 32, 'CSL': 33, 'BMG': 34}

