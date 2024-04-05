#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math
import numpy
import pandas as pd
import datetime as dt
import glob
from scipy import constants
from matplotlib import gridspec
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
# -------------------------------------------------------------------------------------------------------
#	
#	Plots SOLO
#
# --------------------------------------------------------------------------------------------------------


#urSWA = '/Users/cperezal/Documents/SoLo/data/SOLO_L2_SWA-PAS-GRND-MOM_2613226.txt'
urSWA = '/home/arturo/Documentos/SOLO/data/SOLO_L2_SWA-PAS-GRND-MOM_2613226.txt'
icSWA = pd.read_table(urSWA, delim_whitespace=True, skiprows=46)
icSWA.columns = ['year', 'time', 'Np', 'Tp', 'Vr', 'Vt', 'Vn']

#urMAG = '/Users/cperezal/Documents/SoLo/data/SOLO_L2_MAG-RTN-NORMAL-1-MINUTE_2613226.txt'
urMAG = '/home/arturo/Documentos/SOLO/data/SOLO_L2_MAG-RTN-NORMAL-1-MINUTE_2613226.txt'
icMAG = pd.read_table(urMAG, delim_whitespace=True, skiprows=67)
icMAG.columns = ['year', 'time', 'Br', 'Bt', 'Bn']

B = np.sqrt(icMAG['Br']**2 + icMAG['Bt']**2 + icMAG['Bn']**2)
Pp = (icSWA['Np']*1e-6)*icSWA['Tp']*constants.value('Boltzmann constant')
#PB = ((B*1e-9)^2)/(2*1.2566e-6)
#betta = (Pp/PB)*1e12   #betta = (Pp/PB)*1e11




#dateMAG = np.arange(len(icMAG), dtype=float)
dateMAG = ["" for x in range(len(icMAG))]

for x in range(len(icMAG)):
    dateMAG[x] = icMAG['year'][x][6:10]+'-'+icMAG['year'][x][3:5]+'-'+icMAG['year'][x][0:2]+' '+icMAG['time'][x][0:8]
    

srDateMAG = pd.Series(dateMAG)
#df = pd.DataFrame(sr)

icMAG = icMAG.assign(srDateMAG=srDateMAG.values)

#x = np.absolute((lambda3*180.0)/math.pi)
#sr1 = pd.Series(x)
#df1 = pd.DataFrame(sr1)
#df1 = df1.rename(columns = {0:'lambda3'})  df1 = df1.assign(e=e.values)


#----------------------------------------------------------------------------------------------------------------------------
# 	













