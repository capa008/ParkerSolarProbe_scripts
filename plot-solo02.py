#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.dates as dates
import math
import numpy
import pandas as pd
import datetime as dt
import glob
from scipy.optimize import curve_fit
from scipy import constants
from matplotlib import gridspec
from sunpy.time import parse_time
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

Bar = np.arange(len(icMAG), dtype=float)
Var = np.arange(len(icSWA), dtype=float)
betta_ar = np.arange(len(icMAG), dtype=float)

dateSWA = ["" for x in range(len(icSWA))] 
dateMAG = ["" for x in range(len(icMAG))]

for x in range(len(icMAG)):
    dateMAG[x] = icMAG['year'][x][6:10]+'-'+icMAG['year'][x][3:5]+'-'+icMAG['year'][x][0:2]+' '+icMAG['time'][x][0:8]
    Bar[x] =  np.sqrt(icMAG['Br'][x]**2 + icMAG['Bt'][x]**2 + icMAG['Bn'][x]**2)
    Pp = (icSWA['Np'][x]*1e-6)*icSWA['Tp'][x]*constants.value('Boltzmann constant')
    PB = ((Bar[x]*1e-9)**2)/(2*1.2566e-6)
    betta_ar[x] = (Pp/PB)*1e11
    
    #betta_ar[x] =  (( (icSWA['Np'][x]*1e-6)*icSWA['Tp'][x]*constants.value('Boltzmann constant') ) / ((Bar[x]*1e-9)^2)/(2*1.2566e-6) ) *1e12

for x in range(len(icSWA)):
    dateSWA[x] = icSWA['year'][x][6:10]+'-'+icSWA['year'][x][3:5]+'-'+icSWA['year'][x][0:2]+' '+icSWA['time'][x][0:8]
    Var[x] =  np.sqrt(icSWA['Vr'][x]**2 + icSWA['Vt'][x]**2 + icSWA['Vn'][x]**2)


srDateMAG = pd.Series(dateMAG)
icMAG = icMAG.assign(srDateMAG=srDateMAG.values)

srDateSWA = pd.Series(dateSWA)
icSWA = icSWA.assign(srDateSWA=srDateSWA.values)

B = pd.Series(Bar)
icMAG = icMAG.assign(B=B.values)

betta = pd.Series(betta_ar)
icMAG = icMAG.assign(betta=betta.values)

V = pd.Series(Var)
icSWA = icSWA.assign(V=V.values)

# ---------------------------------------
ICME_ti = '2022-09-06 10:01'
ME_ti = '2022-09-07 06:47'
ME_tf = '2022-09-08 04:10'


# ----------------------------------------------------------------------------
# -------- PLOT ---------
#
fig = plt.figure(figsize=(8.0,9.5))
top=0.965
bottom=0.055
left=0.120
right=0.975
hspace=0.070
wspace=0.6

fig.subplots_adjust(top=top,bottom=bottom,left=left,right=right,hspace=hspace, wspace=wspace)
plt.rc('font', size=12)
# ---------------------------------------------
B_avg = icMAG['B'].rolling(window=10).mean()
ax1 = plt.subplot(7, 1,1)
gs = gridspec.GridSpec(7, 3)
icMAG['srDateMAG'] = pd.to_datetime(icMAG['srDateMAG'], format='%Y-%m-%d %H:%M:%S')
#plt.plot(icMAG['srDateMAG'], icMAG['B'], linewidth='0.5')
plt.plot(icMAG['srDateMAG'], B_avg, linewidth='0.5')
formatter = dates.DateFormatter('%Y-%m-%d %H:%M:%S') 
plt.title('SOLO/SWA/MAG', fontsize=18)
plt.ylabel("|B| [nT]")
plt.axvline(pd.to_datetime(ICME_ti), color='black', linestyle='-', lw=2)
plt.axvline(pd.to_datetime(ME_ti), color='black', linestyle='--', lw=2)
plt.axvline(pd.to_datetime(ME_tf), color='black', linestyle='--', lw=2)
plt.axvspan(ME_ti, ME_tf, alpha=0.2)
ax1.axes.xaxis.set_ticklabels([])	
plt.xlim(icMAG['srDateMAG'][0], icMAG['srDateMAG'][len(icMAG['srDateMAG'])-1])
#-----
ax2 = plt.subplot(7, 1,2)
plt.plot(icMAG['srDateMAG'], icMAG['Br'], color='black', linewidth='0.5')
plt.plot(icMAG['srDateMAG'], icMAG['Bt'], 'r-',linewidth='0.5')
plt.plot(icMAG['srDateMAG'], icMAG['Bn'], 'b-',linewidth='0.5')
plt.ylabel(r'$B_{r,t,n} [nT]$')
plt.axvline(pd.to_datetime(ICME_ti), color='black', linestyle='-', lw=2)
plt.axvline(pd.to_datetime(ME_ti), color='black', linestyle='--', lw=2)
plt.axvline(pd.to_datetime(ME_tf), color='black', linestyle='--', lw=2)
plt.axvspan(ME_ti, ME_tf, alpha=0.2)
ax2.axes.xaxis.set_ticklabels([])
plt.xlim(icMAG['srDateMAG'][0], icMAG['srDateMAG'][len(icMAG['srDateMAG'])-1])
# ----		
V_avg = icSWA['V'].rolling(window=100).mean()
ax3 = plt.subplot(7, 1,3)
#plt.plot(icSWA['srDateSWA'], icSWA['V'], linewidth='0.5')
#plt.plot(icSWA['srDateSWA'], V_avg, linewidth='0.5')
plt.ylabel(r'$V_{th} [km/s]$')
plt.axvline(pd.to_datetime(ICME_ti), color='black', linestyle='-', lw=2)
plt.axvline(pd.to_datetime(ME_ti), color='black', linestyle='--', lw=2)
plt.axvline(pd.to_datetime(ME_tf), color='black', linestyle='--', lw=2)
plt.axvspan(ME_ti, ME_tf, alpha=0.2)
ax3.axes.xaxis.set_ticklabels([])
plt.xlim(icMAG['srDateMAG'][0], icMAG['srDateMAG'][len(icMAG['srDateMAG'])-1])
# ----
Np_avg = icSWA['Np'].rolling(window=100).mean()
ax4 = plt.subplot(7, 1,4)
#plt.plot(icSWA['srDateSWA'], icSWA['Np'], linewidth='0.5')
#plt.plot(icSWA['srDateSWA'], Np_avg, linewidth='0.5')
plt.ylabel(r'$N_{p}[\#/cm^{3}]$')
plt.axvline(pd.to_datetime(ICME_ti), color='black', linestyle='-', lw=2)
plt.axvline(pd.to_datetime(ME_ti), color='black', linestyle='--', lw=2)
plt.axvline(pd.to_datetime(ME_tf), color='black', linestyle='--', lw=2)
plt.axvspan(ME_ti, ME_tf, alpha=0.2)
ax4.axes.xaxis.set_ticklabels([])
plt.xlim(icMAG['srDateMAG'][0], icMAG['srDateMAG'][len(icMAG['srDateMAG'])-1])
# ----
Tp_avg = icSWA['Tp'].rolling(window=100).mean() 
ax5 = plt.subplot(7, 1,5)
#plt.plot(icSWA['srDateSWA'], icSWA['Tp'], linewidth='0.5')
#plt.plot(icSWA['srDateSWA'], Tp_avg, linewidth='0.5')
plt.ylabel(r'$T [K]$')
plt.axvline(pd.to_datetime(ICME_ti), color='black', linestyle='-', lw=2)
plt.axvline(pd.to_datetime(ME_ti), color='black', linestyle='--', lw=2)
plt.axvline(pd.to_datetime(ME_tf), color='black', linestyle='--', lw=2)
plt.axvspan(ME_ti, ME_tf, alpha=0.2)
ax5.axes.xaxis.set_ticklabels([])
plt.xlim(icMAG['srDateMAG'][0], icMAG['srDateMAG'][len(icMAG['srDateMAG'])-1])
# ----
betta_avg = icMAG['betta'].rolling(window=100).mean()
ax6 = plt.subplot(7, 1,6)
icMAG['srDateMAG'] = pd.to_datetime(icMAG['srDateMAG'], format='%Y-%m-%d %H:%M:%S')
plt.plot(icMAG['srDateMAG'], icMAG['betta'], linewidth='0.5')
#plt.plot(icMAG['srDateMAG'], betta_avg, linewidth='0.5')
#plt.ylim(0,3)
plt.ylabel(r'$\beta$')
plt.xlabel("mm-dd hh")
plt.axvline(pd.to_datetime(ICME_ti), color='black', linestyle='-', lw=2)
plt.axvline(pd.to_datetime(ME_ti), color='black', linestyle='--', lw=2)
plt.axvline(pd.to_datetime(ME_tf), color='black', linestyle='--', lw=2)
plt.axvspan(ME_ti, ME_tf, alpha=0.2)
plt.xlim(icMAG['srDateMAG'][0], icMAG['srDateMAG'][len(icMAG['srDateMAG'])-1])
plt.tick_params(rotation=45)


plt.show()


# ============================================================================
#   analysis
#




ME = icMAG[icMAG.srDateMAG.ge(pd.to_datetime(ME_ti)) & icMAG.srDateMAG.le(pd.to_datetime(ME_tf))]

print('Mean magnetic field magnitude in ME: ', ME['B'].mean() )

# ---------------------------------------------
icMAG['srDateMAG'] = pd.to_datetime(icMAG['srDateMAG'], format='%Y-%m-%d %H:%M:%S')
plt.plot(ME['srDateMAG'], ME['B'], linewidth='0.5')
#plt.plot(icMAG['srDateMAG'], B_avg, linewidth='0.5')
formatter = dates.DateFormatter('%Y-%m-%d %H:%M:%S') 
plt.title('SOLO/SWA/MAG', fontsize=18)
plt.ylabel("|B| [nT]")
#plt.xlim(ME['srDateMAG'][0], ME['srDateMAG'][len(ME['srDateMAG'])-1])
plt.tick_params(rotation=45)
plt.show()
# ---------------------------------------------


#--icMAG['srDateMAG'] = pd.to_datetime(icMAG['srDateMAG'], format='%Y-%m-%d %H:%M:%S')
#--icMAG.plot(x='srDateMAG', y='Bn')
#--formatter = dates.DateFormatter('%Y-%m-%d %H:%M:%S') 
#--plt.axvline(pd.to_datetime('2022-09-07 06:47'), color='black', linestyle='--', lw=2)
#plt.gcf().axes[0].xaxis.set_major_formatter(formatter)


# ============================================================================
#
#   Magnetic Field Profiles and 
#


punto_inicial = parse_time(ME_ti).plot_date
punto_final = parse_time(ME_tf).plot_date

DateMAGVal = parse_time(srDateMAG).plot_date
srDateMAGVal = pd.Series(DateMAGVal)
icMAG = icMAG.assign(srDateMAGVal=srDateMAGVal.values)
interval = icMAG[icMAG.srDateMAGVal.ge(punto_inicial ) & icMAG.srDateMAGVal.le(punto_final)]

M = interval['srDateMAGVal']
###V =  interval['B']
V = ME['B']


#print(len(M))
#print(len(V2))

def func(x, a, b):
    return a * x**(-b) 

popt, pcov = curve_fit(func, M, V)
#33print(*popt)

#M = pd.to_datetime(M, format='%Y-%m-%d %H:%M:%S')
toplot = np.arange(1,100)

plt.plot(toplot, func(toplot, *popt), '-', label='fit')
#plt.plot(M, V, linewidth='0.5', label = 'B-data')

#plt.plot(M, func(M, *popt), '-', label='fit')

plt.show()





