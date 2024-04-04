#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 11:13:32 2024

@author: cperezal
"""

import pandas as pd
import numpy as np
from scipy import constants
import matplotlib.pyplot as plt
from sunpy.time import parse_time

# -------------------------------
# SoLo data
#
#
# ------------------------------

urSWA = '/Users/cperezal/Documents/SoLo/data/SOLO_L2_SWA-PAS-GRND-MOM_2613226.txt'
icSWA = pd.read_table(urSWA, delim_whitespace=True, skiprows=46)
icSWA.columns = ['year', 'time', 'Np', 'Tp', 'Vr', 'Vt', 'Vn']

urMAG = '/Users/cperezal/Documents/SoLo/data/SOLO_L2_MAG-RTN-NORMAL-1-MINUTE_2613226.txt'
icMAG = pd.read_table(urMAG, delim_whitespace=True, skiprows=67)
icMAG.columns = ['year', 'time', 'Br', 'Bt', 'Bn']

B = np.sqrt(icMAG['Br']**2 + icMAG['Bt']**2 + icMAG['Bn']**2)
Pp = (icSWA['Np']*1e-6)*icSWA['Tp']*constants.value('Boltzmann constant')
#PB = ((B*1e-9)^2)/(2*1.2566e-6)
#betta = (Pp/PB)*1e12   #betta = (Pp/PB)*1e11


dateMAG = np.arange(len(icMAG), dtype=float)
for x in range(len(icMAG)):
    value = icMAG['year'][x][6:10]+'-'+icMAG['year'][x][3:5]+'-'+icMAG['year'][x][0:2]+'T'+icMAG['time'][x][0:12]
    dateMAG[x] = parse_time(value).plot_date
    
    
plt.plot(dateMAG, B)
plt.ylabel('Magnetic field magnitud [nT]')
plt.xlabel('Time')

plt.show()


import matplotlib.dates as dates

icMAG['DateStrings'] = icMAG['year'].dt.strftime('%Y-%m-%d %H:%M:%S')

