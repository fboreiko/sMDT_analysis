# splitter_regions_Run2.py
#  List and functions for splitter regions in Run2 (2016-2018)
#
# Contents:
#  numregions          => Number of regions (208)
#  regionlist[iregion] => has list of chambers in region iregion [1:208]
#  getregion(chamber)  => Return region number of given chamber
#    
#  How to use:
# import splitter_regions_Run2
# splitter_regions_Run2.getregion('BEE_8_-1')   => returns 204
# splitter_regions_Run2.regionlist[20]
#       => returns list: ('BIL_4_3', 'BIL_4_4', 'BML_4_3', 'BML_4_4', 'BOL_4_3', 'BOL_4_4')

numregions = 208
regionlist = '', \
               ('BIL_1_1', 'BIL_1_2', 'BML_1_1', 'BML_1_2', 'BOL_1_1', 'BOL_1_2'), \
               ('BIL_2_1', 'BIL_2_2', 'BML_2_1', 'BML_2_2', 'BOL_2_1', 'BOL_2_2'), \
               ('BIL_3_1', 'BIL_3_2', 'BML_3_1', 'BML_3_2', 'BOL_3_1', 'BOL_3_2'), \
               ('BIL_4_1', 'BIL_4_2', 'BML_4_1', 'BML_4_2', 'BOL_4_1', 'BOL_4_2'), \
               ('BIL_5_1', 'BIL_5_2', 'BML_5_1', 'BML_5_2', 'BOL_5_1', 'BOL_5_2'), \
               ('BIR_6_1', 'BIR_6_2', 'BML_6_1', 'BML_6_2', 'BOL_6_1', 'BOL_6_2'), \
               ('BIL_7_1', 'BIL_7_2', 'BML_7_1', 'BML_7_2', 'BOL_7_1', 'BOL_7_2'), \
               ('BIR_8_1', 'BIR_8_2', 'BML_8_1', 'BML_8_2', 'BOL_8_1', 'BOL_8_2'), \
               ('BIS_1_1', 'BIS_1_2', 'BMS_1_1', 'BMS_1_2', 'BOS_1_1', 'BOS_1_2'), \
               ('BIS_2_1', 'BIS_2_2', 'BMS_2_1', 'BMS_2_2', 'BOS_2_1', 'BOS_2_2'), \
               ('BIS_3_1', 'BIS_3_2', 'BMS_3_1', 'BMS_3_2', 'BOS_3_1', 'BOS_3_2'), \
               ('BIS_4_1', 'BIS_4_2', 'BMS_4_1', 'BMS_4_2', 'BOS_4_1', 'BOS_4_2'), \
               ('BIS_5_1', 'BIS_5_2', 'BMS_5_1', 'BMS_5_2', 'BOS_5_1', 'BOS_5_2'), \
               ('BIS_6_1', 'BIS_6_2', 'BMF_6_1', 'BOF_6_1', 'BOG_6_0', 'BOG_6_1'), \
               ('BIS_7_1', 'BIS_7_2', 'BMF_7_1', 'BOF_7_1', 'BOG_7_0', 'BOG_7_1'), \
               ('BIS_8_1', 'BIS_8_2', 'BMS_8_1', 'BMS_8_2', 'BOS_8_1', 'BOS_8_2'), \
               ('BIL_1_3', 'BIL_1_4', 'BML_1_3', 'BML_1_4', 'BOL_1_3', 'BOL_1_4'), \
               ('BIL_2_3', 'BIL_2_4', 'BML_2_3', 'BML_2_4', 'BOL_2_3', 'BOL_2_4'), \
               ('BIL_3_3', 'BIL_3_4', 'BML_3_3', 'BML_3_4', 'BOL_3_3', 'BOL_3_4'), \
               ('BIL_4_3', 'BIL_4_4', 'BML_4_3', 'BML_4_4', 'BOL_4_3', 'BOL_4_4'), \
               ('BIL_5_3', 'BIL_5_4', 'BML_5_3', 'BML_5_4', 'BOL_5_3', 'BOL_5_4'), \
               ('BIR_6_3', 'BIR_6_4', 'BML_6_3', 'BML_6_4', 'BOL_6_3', 'BOL_6_4'), \
               ('BIL_7_3', 'BIL_7_4', 'BML_7_3', 'BOL_7_3', 'BOL_7_4'), \
               ('BIR_8_3', 'BIR_8_4', 'BML_8_3', 'BML_8_4', 'BOL_8_3', 'BOL_8_4'), \
               ('BIS_1_3', 'BIS_1_4', 'BMS_1_3', 'BMS_1_4', 'BOS_1_3', 'BOS_1_4'), \
               ('BIS_2_3', 'BIS_2_4', 'BMS_2_3', 'BMS_2_4', 'BOS_2_3', 'BOS_2_4'), \
               ('BIS_3_3', 'BIS_3_4', 'BMS_3_3', 'BMS_3_4', 'BOS_3_3', 'BOS_3_4'), \
               ('BIS_4_3', 'BIS_4_4', 'BMS_4_3', 'BMS_4_4', 'BOS_4_3', 'BOS_4_4'), \
               ('BIS_5_3', 'BIS_5_4', 'BMS_5_3', 'BMS_5_4', 'BOS_5_3', 'BOS_5_4'), \
               ('BIS_6_3', 'BIS_6_4', 'BMF_6_2', 'BOF_6_2', 'BOF_6_3', 'BOG_6_2'), \
               ('BIS_7_3', 'BIS_7_4', 'BMF_7_2', 'BOF_7_2', 'BOF_7_3', 'BOG_7_2'), \
               ('BIS_8_3', 'BIS_8_4', 'BMS_8_3', 'BMS_8_4', 'BOS_8_3', 'BOS_8_4'), \
               ('BIL_1_5', 'BIL_1_6', 'BML_1_5', 'BML_1_6', 'BOL_1_5', 'BOL_1_6'), \
               ('BIL_2_5', 'BIL_2_6', 'BML_2_5', 'BML_2_6', 'BOL_2_5', 'BOL_2_6'), \
               ('BIL_3_5', 'BIL_3_6', 'BML_3_5', 'BML_3_6', 'BOL_3_5', 'BOL_3_6'), \
               ('BIL_4_5', 'BIL_4_6', 'BML_4_5', 'BML_4_6', 'BOL_4_5', 'BOL_4_6'), \
               ('BIL_5_5', 'BIL_5_6', 'BML_5_5', 'BML_5_6', 'BOL_5_5', 'BOL_5_6'), \
               ('BIR_6_5', 'BIR_6_6', 'BML_6_5', 'BML_6_6', 'BOL_6_5', 'BOL_6_6'), \
               ('BIL_7_5', 'BIL_7_6', 'BML_7_4', 'BML_7_5', 'BOL_7_5', 'BOL_7_6'), \
               ('BIR_8_5', 'BIR_8_6', 'BML_8_5', 'BML_8_6', 'BOL_8_5', 'BOL_8_6'), \
               ('BIS_1_5', 'BIS_1_6', 'BMS_1_5', 'BMS_1_6', 'BOS_1_5', 'BOS_1_6'), \
               ('BIS_2_5', 'BIS_2_6', 'BMS_2_5', 'BMS_2_6', 'BOS_2_5', 'BOS_2_6'), \
               ('BIS_3_5', 'BIS_3_6', 'BMS_3_5', 'BMS_3_6', 'BOS_3_5', 'BOS_3_6'), \
               ('BIS_4_5', 'BIS_4_6', 'BMS_4_5', 'BMS_4_6', 'BOS_4_5', 'BOS_4_6'), \
               ('BIS_5_5', 'BIS_5_6', 'BMS_5_5', 'BMS_5_6', 'BOS_5_5', 'BOS_5_6'), \
               ('BIS_6_5', 'BIS_6_6', 'BMF_6_3', 'BOF_6_4', 'BOG_6_3', 'BOG_6_4'), \
               ('BIS_7_5', 'BIS_7_6', 'BMF_7_3', 'BOF_7_4', 'BOG_7_3', 'BOG_7_4'), \
               ('BIS_8_5', 'BIS_8_6', 'BMS_8_5', 'BMS_8_6', 'BOS_8_5', 'BOS_8_6'), \
               ('BIM_6_1', 'BIM_6_2', 'BIM_6_3', 'BIM_6_4', 'BIM_6_5'), \
               ('BIM_8_1', 'BIM_8_2', 'BIM_8_3', 'BIM_8_4', 'BIM_8_5'), \
               ('BME_7_1', 'BMG_6_1', 'BMG_6_2', 'BMG_6_3'), \
               ('BOL_7_7', 'BMG_7_1', 'BMG_7_2', 'BMG_7_3'), \
               ('BIL_1_-1', 'BIL_1_-2', 'BML_1_-1', 'BML_1_-2', 'BOL_1_-1', 'BOL_1_-2'), \
               ('BIL_2_-1', 'BIL_2_-2', 'BML_2_-1', 'BML_2_-2', 'BOL_2_-1', 'BOL_2_-2'), \
               ('BIL_3_-1', 'BIL_3_-2', 'BML_3_-1', 'BML_3_-2', 'BOL_3_-1', 'BOL_3_-2'), \
               ('BIL_4_-1', 'BIL_4_-2', 'BML_4_-1', 'BML_4_-2', 'BOL_4_-1', 'BOL_4_-2'), \
               ('BIL_5_-1', 'BIL_5_-2', 'BML_5_-1', 'BML_5_-2', 'BOL_5_-1', 'BOL_5_-2'), \
               ('BIR_6_-1', 'BIR_6_-2', 'BML_6_-1', 'BML_6_-2', 'BOL_6_-1', 'BOL_6_-2'), \
               ('BIL_7_-1', 'BIL_7_-2', 'BML_7_-1', 'BML_7_-2', 'BOL_7_-1', 'BOL_7_-2'), \
               ('BIR_8_-1', 'BIR_8_-2', 'BML_8_-1', 'BML_8_-2', 'BOL_8_-1', 'BOL_8_-2'), \
               ('BIS_1_-1', 'BIS_1_-2', 'BMS_1_-1', 'BMS_1_-2', 'BOS_1_-1', 'BOS_1_-2'), \
               ('BIS_2_-1', 'BIS_2_-2', 'BMS_2_-1', 'BMS_2_-2', 'BOS_2_-1', 'BOS_2_-2'), \
               ('BIS_3_-1', 'BIS_3_-2', 'BMS_3_-1', 'BMS_3_-2', 'BOS_3_-1', 'BOS_3_-2'), \
               ('BIS_4_-1', 'BIS_4_-2', 'BMS_4_-1', 'BMS_4_-2', 'BOS_4_-1', 'BOS_4_-2'), \
               ('BIS_5_-1', 'BIS_5_-2', 'BMS_5_-1', 'BMS_5_-2', 'BOS_5_-1', 'BOS_5_-2'), \
               ('BIS_6_-1', 'BIS_6_-2', 'BMF_6_-1', 'BOF_6_-1', 'BOG_6_-1'), \
               ('BIS_7_-1', 'BIS_7_-2', 'BMF_7_-1', 'BOF_7_-1', 'BOG_7_-1'), \
               ('BIS_8_-1', 'BIS_8_-2', 'BMS_8_-1', 'BMS_8_-2', 'BOS_8_-1', 'BOS_8_-2'), \
               ('BIL_1_-3', 'BIL_1_-4', 'BML_1_-3', 'BML_1_-4', 'BOL_1_-3', 'BOL_1_-4'), \
               ('BIL_2_-3', 'BIL_2_-4', 'BML_2_-3', 'BML_2_-4', 'BOL_2_-3', 'BOL_2_-4'), \
               ('BIL_3_-3', 'BIL_3_-4', 'BML_3_-3', 'BML_3_-4', 'BOL_3_-3', 'BOL_3_-4'), \
               ('BIL_4_-3', 'BIL_4_-4', 'BML_4_-3', 'BML_4_-4', 'BOL_4_-3', 'BOL_4_-4'), \
               ('BIL_5_-3', 'BIL_5_-4', 'BML_5_-3', 'BML_5_-4', 'BOL_5_-3', 'BOL_5_-4'), \
               ('BIR_6_-3', 'BIR_6_-4', 'BML_6_-3', 'BML_6_-4', 'BOL_6_-3', 'BOL_6_-4'), \
               ('BIL_7_-3', 'BIL_7_-4', 'BML_7_-3', 'BOL_7_-3', 'BOL_7_-4'), \
               ('BIR_8_-3', 'BIR_8_-4', 'BML_8_-3', 'BML_8_-4', 'BOL_8_-3', 'BOL_8_-4'), \
               ('BIS_1_-3', 'BIS_1_-4', 'BMS_1_-3', 'BMS_1_-4', 'BOS_1_-3', 'BOS_1_-4'), \
               ('BIS_2_-3', 'BIS_2_-4', 'BMS_2_-3', 'BMS_2_-4', 'BOS_2_-3', 'BOS_2_-4'), \
               ('BIS_3_-3', 'BIS_3_-4', 'BMS_3_-3', 'BMS_3_-4', 'BOS_3_-3', 'BOS_3_-4'), \
               ('BIS_4_-3', 'BIS_4_-4', 'BMS_4_-3', 'BMS_4_-4', 'BOS_4_-3', 'BOS_4_-4'), \
               ('BIS_5_-3', 'BIS_5_-4', 'BMS_5_-3', 'BMS_5_-4', 'BOS_5_-3', 'BOS_5_-4'), \
               ('BIS_6_-3', 'BIS_6_-4', 'BMF_6_-2', 'BOF_6_-2', 'BOF_6_-3', 'BOG_6_-2'), \
               ('BIS_7_-3', 'BIS_7_-4', 'BMF_7_-2', 'BOF_7_-2', 'BOF_7_-3', 'BOG_7_-2'), \
               ('BIS_8_-3', 'BIS_8_-4', 'BMS_8_-3', 'BMS_8_-4', 'BOS_8_-3', 'BOS_8_-4'), \
               ('BIL_1_-5', 'BIL_1_-6', 'BML_1_-5', 'BML_1_-6', 'BOL_1_-5', 'BOL_1_-6'), \
               ('BIL_2_-5', 'BIL_2_-6', 'BML_2_-5', 'BML_2_-6', 'BOL_2_-5', 'BOL_2_-6'), \
               ('BIL_3_-5', 'BIL_3_-6', 'BML_3_-5', 'BML_3_-6', 'BOL_3_-5', 'BOL_3_-6'), \
               ('BIL_4_-5', 'BIL_4_-6', 'BML_4_-5', 'BML_4_-6', 'BOL_4_-5', 'BOL_4_-6'), \
               ('BIL_5_-5', 'BIL_5_-6', 'BML_5_-5', 'BML_5_-6', 'BOL_5_-5', 'BOL_5_-6'), \
               ('BIR_6_-5', 'BIR_6_-6', 'BML_6_-5', 'BML_6_-6', 'BOL_6_-5', 'BOL_6_-6'), \
               ('BIL_7_-5', 'BIL_7_-6', 'BML_7_-4', 'BML_7_-5', 'BOL_7_-5', 'BOL_7_-6'), \
               ('BIR_8_-5', 'BIR_8_-6', 'BML_8_-5', 'BML_8_-6', 'BOL_8_-5', 'BOL_8_-6'), \
               ('BIS_1_-5', 'BIS_1_-6', 'BMS_1_-5', 'BMS_1_-6', 'BOS_1_-5', 'BOS_1_-6'), \
               ('BIS_2_-5', 'BIS_2_-6', 'BMS_2_-5', 'BMS_2_-6', 'BOS_2_-5', 'BOS_2_-6'), \
               ('BIS_3_-5', 'BIS_3_-6', 'BMS_3_-5', 'BMS_3_-6', 'BOS_3_-5', 'BOS_3_-6'), \
               ('BIS_4_-5', 'BIS_4_-6', 'BMS_4_-5', 'BMS_4_-6', 'BOS_4_-5', 'BOS_4_-6'), \
               ('BIS_5_-5', 'BIS_5_-6', 'BMS_5_-5', 'BMS_5_-6', 'BOS_5_-5', 'BOS_5_-6'), \
               ('BIS_6_-5', 'BIS_6_-6', 'BMF_6_-3', 'BOF_6_-4', 'BOG_6_-3', 'BOG_6_-4'), \
               ('BIS_7_-5', 'BIS_7_-6', 'BMF_7_-3', 'BOF_7_-4', 'BOG_7_-3', 'BOG_7_-4'), \
               ('BIS_8_-5', 'BIS_8_-6', 'BMS_8_-5', 'BMS_8_-6', 'BOS_8_-5', 'BOS_8_-6'), \
               ('BIM_6_-1', 'BIM_6_-2', 'BIM_6_-3', 'BIM_6_-4', 'BIM_6_-5'), \
               ('BIM_8_-1', 'BIM_8_-2', 'BIM_8_-3', 'BIM_8_-4', 'BIM_8_-5'), \
               ('BME_7_-1', 'BMG_6_-1', 'BMG_6_-2', 'BMG_6_-3'), \
               ('BOL_7_-7', 'BMG_7_-1', 'BMG_7_-2', 'BMG_7_-3'), \
               ('EIL_1_5', 'EIL_1_4', 'EEL_1_1', 'EEL_1_2', 'EML_1_4', 'EML_1_5'), \
               ('EIL_2_4', 'EEL_2_1', 'EEL_2_2', 'EML_2_4', 'EML_2_5'), \
               ('EIL_3_4', 'EEL_3_1', 'EML_3_4', 'EML_3_5'), \
               ('EIL_4_4', 'EEL_4_1', 'EEL_4_2', 'EML_4_4', 'EML_4_5'), \
               ('EIL_5_5', 'EIL_5_4', 'EEL_5_1', 'EEL_5_2', 'EML_5_4', 'EML_5_5'), \
               ('EIL_6_4', 'EEL_6_1', 'EEL_6_2', 'EML_6_4', 'EML_6_5'), \
               ('EIL_7_4', 'EEL_7_1', 'EEL_7_2', 'EML_7_4', 'EML_7_5'), \
               ('EIL_8_4', 'EEL_8_1', 'EEL_8_2', 'EML_8_4', 'EML_8_5'), \
               ('BIS_1_8', 'BIS_1_7', 'EES_1_1', 'EES_1_2', 'EMS_1_4', 'EMS_1_5'), \
               ('BIS_2_8', 'BIS_2_7', 'EES_2_1', 'EES_2_2', 'EMS_2_4', 'EMS_2_5'), \
               ('BIS_3_8', 'BIS_3_7', 'EES_3_1', 'EES_3_2', 'EMS_3_4', 'EMS_3_5'), \
               ('BIS_4_8', 'BIS_4_7', 'EES_4_1', 'EES_4_2', 'EMS_4_4', 'EMS_4_5'), \
               ('BIS_5_8', 'BIS_5_7', 'EES_5_1', 'EES_5_2', 'EMS_5_4', 'EMS_5_5'), \
               ('BIS_6_8', 'BIS_6_7', 'EES_6_1', 'EES_6_2', 'EMS_6_4', 'EMS_6_5'), \
               ('BIS_7_8', 'BIS_7_7', 'EES_7_1', 'EES_7_2', 'EMS_7_4', 'EMS_7_5'), \
               ('BIS_8_8', 'BIS_8_7', 'EES_8_1', 'EES_8_2', 'EMS_8_4', 'EMS_8_5'), \
               ('EIL_1_3', 'EIL_1_2', 'EML_1_3', 'EOL_1_4', 'EOL_1_5', 'EOL_1_6'), \
               ('EIL_2_3', 'EIL_2_2', 'EML_2_3', 'EOL_2_4', 'EOL_2_5', 'EOL_2_6'), \
               ('EIL_3_3', 'EIL_3_2', 'EML_3_3', 'EOL_3_4', 'EOL_3_5', 'EOL_3_6'), \
               ('EIL_4_3', 'EIL_4_2', 'EML_4_3', 'EOL_4_4', 'EOL_4_5', 'EOL_4_6'), \
               ('EIL_5_3', 'EIL_5_2', 'EML_5_3', 'EOL_5_4', 'EOL_5_5', 'EOL_5_6'), \
               ('EIL_6_3', 'EIL_6_2', 'EML_6_3', 'EOL_6_4', 'EOL_6_5', 'EOL_6_6'), \
               ('EIL_7_3', 'EIL_7_2', 'EML_7_3', 'EOL_7_4', 'EOL_7_5', 'EOL_7_6'), \
               ('EIL_8_3', 'EIL_8_2', 'EML_8_3', 'EOL_8_4', 'EOL_8_5', 'EOL_8_6'), \
               ('EIS_1_1', 'EIS_1_2', 'EMS_1_3', 'EOS_1_4', 'EOS_1_5', 'EOS_1_6'), \
               ('EIS_2_1', 'EIS_2_2', 'EMS_2_3', 'EOS_2_4', 'EOS_2_5', 'EOS_2_6'), \
               ('EIS_3_1', 'EIS_3_2', 'EMS_3_3', 'EOS_3_4', 'EOS_3_5', 'EOS_3_6'), \
               ('EIS_4_1', 'EIS_4_2', 'EMS_4_3', 'EOS_4_4', 'EOS_4_5', 'EOS_4_6'), \
               ('EIS_5_1', 'EIS_5_2', 'EMS_5_3', 'EOS_5_4', 'EOS_5_5', 'EOS_5_6'), \
               ('EIS_6_1', 'EIS_6_2', 'EMS_6_3', 'EOS_6_4', 'EOS_6_5', 'EOS_6_6'), \
               ('EIS_7_1', 'EIS_7_2', 'EMS_7_3', 'EOS_7_4', 'EOS_7_5', 'EOS_7_6'), \
               ('EIS_8_1', 'EIS_8_2', 'EMS_8_3', 'EOS_8_4', 'EOS_8_5', 'EOS_8_6'), \
               ('EML_1_1', 'EML_1_2', 'EOL_1_1', 'EOL_1_2', 'EOL_1_3'), \
               ('EML_2_1', 'EML_2_2', 'EOL_2_1', 'EOL_2_2', 'EOL_2_3'), \
               ('EML_3_1', 'EML_3_2', 'EOL_3_1', 'EOL_3_2', 'EOL_3_3'), \
               ('EML_4_1', 'EML_4_2', 'EOL_4_1', 'EOL_4_2', 'EOL_4_3'), \
               ('EML_5_1', 'EML_5_2', 'EOL_5_1', 'EOL_5_2', 'EOL_5_3'), \
               ('EML_6_1', 'EML_6_2', 'EOL_6_1', 'EOL_6_2', 'EOL_6_3'), \
               ('EML_7_1', 'EML_7_2', 'EOL_7_1', 'EOL_7_2', 'EOL_7_3'), \
               ('EML_8_1', 'EML_8_2', 'EOL_8_1', 'EOL_8_2', 'EOL_8_3'), \
               ('EMS_1_1', 'EMS_1_2', 'EOS_1_1', 'EOS_1_2', 'EOS_1_3'), \
               ('EMS_2_1', 'EMS_2_2', 'EOS_2_1', 'EOS_2_2', 'EOS_2_3'), \
               ('EMS_3_1', 'EMS_3_2', 'EOS_3_1', 'EOS_3_2', 'EOS_3_3'), \
               ('EMS_4_1', 'EMS_4_2', 'EOS_4_1', 'EOS_4_2', 'EOS_4_3'), \
               ('EMS_5_1', 'EMS_5_2', 'EOS_5_1', 'EOS_5_2', 'EOS_5_3'), \
               ('EMS_6_1', 'EMS_6_2', 'EOS_6_1', 'EOS_6_2', 'EOS_6_3'), \
               ('EMS_7_1', 'EMS_7_2', 'EOS_7_1', 'EOS_7_2', 'EOS_7_3'), \
               ('EMS_8_1', 'EMS_8_2', 'EOS_8_1', 'EOS_8_2', 'EOS_8_3'), \
               ('BEE_1_2', 'BEE_1_1', 'BEE_2_2', 'BEE_2_1', 'EIL_1_1', 'EIL_2_1'), \
               ('BEE_3_2', 'BEE_3_1', 'BEE_4_2', 'BEE_4_1', 'EIL_3_1', 'EIL_4_1'), \
               ('BEE_5_2', 'BEE_5_1', 'BEE_6_2', 'BEE_6_1', 'EIL_5_1', 'EIL_6_1'), \
               ('BEE_7_2', 'BEE_7_1', 'BEE_8_2', 'BEE_8_1', 'EIL_7_1', 'EIL_8_1'), \
               ('EIL_1_-5', 'EIL_1_-4', 'EEL_1_-1', 'EEL_1_-2', 'EML_1_-4', 'EML_1_-5'), \
               ('EIL_2_-4', 'EEL_2_-1', 'EEL_2_-2', 'EML_2_-4', 'EML_2_-5'), \
               ('EIL_3_-4', 'EEL_3_-1', 'EML_3_-4', 'EML_3_-5'), \
               ('EIL_4_-4', 'EEL_4_-1', 'EEL_4_-2', 'EML_4_-4', 'EML_4_-5'), \
               ('EIL_5_-5', 'EIL_5_-4', 'EEL_5_-1', 'EEL_5_-2', 'EML_5_-4', 'EML_5_-5'), \
               ('EIL_6_-4', 'EEL_6_-1', 'EEL_6_-2', 'EML_6_-4', 'EML_6_-5'), \
               ('EIL_7_-4', 'EEL_7_-1', 'EEL_7_-2', 'EML_7_-4', 'EML_7_-5'), \
               ('EIL_8_-4', 'EEL_8_-1', 'EEL_8_-2', 'EML_8_-4', 'EML_8_-5'), \
               ('BIS_1_-8', 'BIS_1_-7', 'EES_1_-1', 'EES_1_-2', 'EMS_1_-4', 'EMS_1_-5'), \
               ('BIS_2_-8', 'BIS_2_-7', 'EES_2_-1', 'EES_2_-2', 'EMS_2_-4', 'EMS_2_-5'), \
               ('BIS_3_-8', 'BIS_3_-7', 'EES_3_-1', 'EES_3_-2', 'EMS_3_-4', 'EMS_3_-5'), \
               ('BIS_4_-8', 'BIS_4_-7', 'EES_4_-1', 'EES_4_-2', 'EMS_4_-4', 'EMS_4_-5'), \
               ('BIS_5_-8', 'BIS_5_-7', 'EES_5_-1', 'EES_5_-2', 'EMS_5_-4', 'EMS_5_-5'), \
               ('BIS_6_-8', 'BIS_6_-7', 'EES_6_-1', 'EES_6_-2', 'EMS_6_-4', 'EMS_6_-5'), \
               ('BIS_7_-8', 'BIS_7_-7', 'EES_7_-1', 'EES_7_-2', 'EMS_7_-4', 'EMS_7_-5'), \
               ('BIS_8_-8', 'BIS_8_-7', 'EES_8_-1', 'EES_8_-2', 'EMS_8_-4', 'EMS_8_-5'), \
               ('EIL_1_-3', 'EIL_1_-2', 'EML_1_-3', 'EOL_1_-4', 'EOL_1_-5', 'EOL_1_-6'), \
               ('EIL_2_-3', 'EIL_2_-2', 'EML_2_-3', 'EOL_2_-4', 'EOL_2_-5', 'EOL_2_-6'), \
               ('EIL_3_-3', 'EIL_3_-2', 'EML_3_-3', 'EOL_3_-4', 'EOL_3_-5', 'EOL_3_-6'), \
               ('EIL_4_-3', 'EIL_4_-2', 'EML_4_-3', 'EOL_4_-4', 'EOL_4_-5', 'EOL_4_-6'), \
               ('EIL_5_-3', 'EIL_5_-2', 'EML_5_-3', 'EOL_5_-4', 'EOL_5_-5', 'EOL_5_-6'), \
               ('EIL_6_-3', 'EIL_6_-2', 'EML_6_-3', 'EOL_6_-4', 'EOL_6_-5', 'EOL_6_-6'), \
               ('EIL_7_-3', 'EIL_7_-2', 'EML_7_-3', 'EOL_7_-4', 'EOL_7_-5', 'EOL_7_-6'), \
               ('EIL_8_-3', 'EIL_8_-2', 'EML_8_-3', 'EOL_8_-4', 'EOL_8_-5', 'EOL_8_-6'), \
               ('EIS_1_-1', 'EIS_1_-2', 'EMS_1_-3', 'EOS_1_-4', 'EOS_1_-5', 'EOS_1_-6'), \
               ('EIS_2_-1', 'EIS_2_-2', 'EMS_2_-3', 'EOS_2_-4', 'EOS_2_-5', 'EOS_2_-6'), \
               ('EIS_3_-1', 'EIS_3_-2', 'EMS_3_-3', 'EOS_3_-4', 'EOS_3_-5', 'EOS_3_-6'), \
               ('EIS_4_-1', 'EIS_4_-2', 'EMS_4_-3', 'EOS_4_-4', 'EOS_4_-5', 'EOS_4_-6'), \
               ('EIS_5_-1', 'EIS_5_-2', 'EMS_5_-3', 'EOS_5_-4', 'EOS_5_-5', 'EOS_5_-6'), \
               ('EIS_6_-1', 'EIS_6_-2', 'EMS_6_-3', 'EOS_6_-4', 'EOS_6_-5', 'EOS_6_-6'), \
               ('EIS_7_-1', 'EIS_7_-2', 'EMS_7_-3', 'EOS_7_-4', 'EOS_7_-5', 'EOS_7_-6'), \
               ('EIS_8_-1', 'EIS_8_-2', 'EMS_8_-3', 'EOS_8_-4', 'EOS_8_-5', 'EOS_8_-6'), \
               ('EML_1_-1', 'EML_1_-2', 'EOL_1_-1', 'EOL_1_-2', 'EOL_1_-3'), \
               ('EML_2_-1', 'EML_2_-2', 'EOL_2_-1', 'EOL_2_-2', 'EOL_2_-3'), \
               ('EML_3_-1', 'EML_3_-2', 'EOL_3_-1', 'EOL_3_-2', 'EOL_3_-3'), \
               ('EML_4_-1', 'EML_4_-2', 'EOL_4_-1', 'EOL_4_-2', 'EOL_4_-3'), \
               ('EML_5_-1', 'EML_5_-2', 'EOL_5_-1', 'EOL_5_-2', 'EOL_5_-3'), \
               ('EML_6_-1', 'EML_6_-2', 'EOL_6_-1', 'EOL_6_-2', 'EOL_6_-3'), \
               ('EML_7_-1', 'EML_7_-2', 'EOL_7_-1', 'EOL_7_-2', 'EOL_7_-3'), \
               ('EML_8_-1', 'EML_8_-2', 'EOL_8_-1', 'EOL_8_-2', 'EOL_8_-3'), \
               ('EMS_1_-1', 'EMS_1_-2', 'EOS_1_-1', 'EOS_1_-2', 'EOS_1_-3'), \
               ('EMS_2_-1', 'EMS_2_-2', 'EOS_2_-1', 'EOS_2_-2', 'EOS_2_-3'), \
               ('EMS_3_-1', 'EMS_3_-2', 'EOS_3_-1', 'EOS_3_-2', 'EOS_3_-3'), \
               ('EMS_4_-1', 'EMS_4_-2', 'EOS_4_-1', 'EOS_4_-2', 'EOS_4_-3'), \
               ('EMS_5_-1', 'EMS_5_-2', 'EOS_5_-1', 'EOS_5_-2', 'EOS_5_-3'), \
               ('EMS_6_-1', 'EMS_6_-2', 'EOS_6_-1', 'EOS_6_-2', 'EOS_6_-3'), \
               ('EMS_7_-1', 'EMS_7_-2', 'EOS_7_-1', 'EOS_7_-2', 'EOS_7_-3'), \
               ('EMS_8_-1', 'EMS_8_-2', 'EOS_8_-1', 'EOS_8_-2', 'EOS_8_-3'), \
               ('BEE_1_-2', 'BEE_1_-1', 'BEE_2_-2', 'BEE_2_-1', 'EIL_1_-1', 'EIL_2_-1'), \
               ('BEE_3_-2', 'BEE_3_-1', 'BEE_4_-2', 'BEE_4_-1', 'EIL_3_-1', 'EIL_4_-1'), \
               ('BEE_5_-2', 'BEE_5_-1', 'BEE_6_-2', 'BEE_6_-1', 'EIL_5_-1', 'EIL_6_-1'), \
               ('BEE_7_-2', 'BEE_7_-1', 'BEE_8_-2', 'BEE_8_-1', 'EIL_7_-1', 'EIL_8_-1')        

#  Return region of given chamber
def getregion(chamber):
  for iregion in range(1,numregions+1):
    if chamber in regionlist[iregion]:
      return iregion
  return 0  