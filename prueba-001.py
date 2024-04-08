#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 23:45:01 2024

@author: arturo
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

M = np.array([730,910,1066,1088,1150], dtype=float)
V = np.array([95.71581923, 146.18564513, 164.46723727, 288.49796413, 370.98703941], dtype=float)

def func(x, a, b, c):
    return a * np.exp(b * x) + c

popt, pcov = curve_fit(func, M, V, [0,0,1], maxfev=100000000)
print(*popt)

fig, ax = plt.subplots()
fig.dpi = 80

ax.plot(M, V, 'go', label='data')
toplot = np.arange(700,1200)
ax.plot(toplot, func(toplot, *popt), '-', label='fit')

plt.xlabel("M")
plt.ylabel("V")
plt.grid()
plt.legend()
plt.show()


# ----------------------------------------------------------------
import pandas as pd

urMAG = '/home/arturo/Documentos/SOLO/data/SOLO_L2_MAG-RTN-NORMAL-1-MINUTE_2613226.txt'
icMAG = pd.read_table(urMAG, delim_whitespace=True, skiprows=67)
icMAG.columns = ['year', 'time', 'Br', 'Bt', 'Bn']

Bar = np.arange(len(icMAG), dtype=float)
dateMAG = ["" for x in range(len(icMAG))]
for x in range(len(icMAG)):
    dateMAG[x] = icMAG['year'][x][6:10]+'-'+icMAG['year'][x][3:5]+'-'+icMAG['year'][x][0:2]+' '+icMAG['time'][x][0:8]
    Bar[x] =  np.sqrt(icMAG['Br'][x]**2 + icMAG['Bt'][x]**2 + icMAG['Bn'][x]**2)

srDateMAG = pd.Series(dateMAG)
icMAG = icMAG.assign(srDateMAG=srDateMAG.values)
B = pd.Series(Bar)
icMAG = icMAG.assign(B=B.values)

ME_ti = '2022-09-07 06:47'
ME_tf = '2022-09-08 04:10'

ME = icMAG[icMAG.srDateMAG.ge(pd.to_datetime(ME_ti)) & icMAG.srDateMAG.le(pd.to_datetime(ME_tf))]

punto_inicial = parse_time(ME_ti).plot_date
punto_final = parse_time(ME_tf).plot_date

DateMAGVal = parse_time(srDateMAG).plot_date
srDateMAGVal = pd.Series(DateMAGVal)
icMAG = icMAG.assign(srDateMAGVal=srDateMAGVal.values)
interval = icMAG[icMAG.srDateMAGVal.ge(punto_inicial ) & icMAG.srDateMAGVal.le(punto_final)]
















