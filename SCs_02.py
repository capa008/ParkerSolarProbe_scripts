echo "# ParkerSolarProbe_scripts" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/capa008/ParkerSolarProbe_scripts.git
git push -u origin main

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 22:56:16 2024

@author: cperezal
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sunpy.time import parse_time

# -----------------------------------------
# Voyager list -ICMEs
icV = pd.read_table('/Users/cperezal/Documents/Spacecraft_statistical/voyager2_icmes.txt',delim_whitespace=True, skiprows=1)
icV.columns = ['year','time','duration','distance','heliolongitude', 'heliolatitude']


# Pioneers list - ICME/shocks
icP = pd.read_table('/Users/cperezal/Documents/Spacecraft_statistical/pioners_icmes.txt',delim_whitespace=True, skiprows=4)
icP.columns = ['SC','shock','date','time', 'speed', 'speed_shock', 'distance', 'heliolatitude', 'heliolongitude' ]


# HeliosA/B list - ICME/shocks
icH = pd.read_table('/Users/cperezal/Documents/Spacecraft_statistical/shocks_20240229_032750.dat',delim_whitespace=True, skiprows=13)
icH.columns = ['yy','mm','dd','hh','mm','ss','sc','distance','heliolatitude', 'heliolongitude' , 'scc', 'sh']



# -----------------------------------------


#url='https://helioforecast.space/static/sync/icmecat/HELIO4CAST_ICMECAT_v21.csv'

ur = '/Users/cperezal/Documents/Spacecraft_statistical/HELIO4CAST_ICMECAT_v22.csv'

ic=pd.read_csv(ur)
ic=ic.drop(columns='Unnamed: 0')

ista=np.where(ic.sc_insitu=='STEREO-A')[0]
istb=np.where(ic.sc_insitu=='STEREO-B')[0]
ipsp=np.where(ic.sc_insitu=='PSP')[0]
imes=np.where(ic.sc_insitu=='MESSENGER')[0]
iwin=np.where(ic.sc_insitu=='Wind')[0]
isol=np.where(ic.sc_insitu=='SolarOrbiter')[0]
iuly=np.where(ic.sc_insitu=='ULYSSES')[0]

# ****************************************************************************
#2018-01-01T00:00Z
fig=plt.figure(3,figsize=(12,8),dpi=80)
ic_mo_start_time_num=parse_time(ic.mo_start_time).plot_date

plt.plot()


plt.plot_date(ic_mo_start_time_num[ista],ic.mo_sc_heliodistance[ista],'ok',c='red',markersize=3,label = 'STA')
plt.plot_date(ic_mo_start_time_num[istb],ic.mo_sc_heliodistance[istb],'ok',c='blue',markersize=3,label = 'STB')
plt.plot_date(ic_mo_start_time_num[ipsp],ic.mo_sc_heliodistance[ipsp],'ok',c='black',markersize=3,label = 'PSP')
plt.plot_date(ic_mo_start_time_num[imes],ic.mo_sc_heliodistance[imes],'ok',c='mediumseagreen',markersize=3,label = 'Wind')
plt.plot_date(ic_mo_start_time_num[iwin],ic.mo_sc_heliodistance[iwin],'ok',c='dimgrey',markersize=3,label = 'Messenger')
plt.plot_date(ic_mo_start_time_num[isol],ic.mo_sc_heliodistance[isol],'ok',c='brown',markersize=3,label = 'Solar Orbiter')
plt.plot_date(ic_mo_start_time_num[imes],ic.mo_sc_heliodistance[imes],'ok',c='dimgrey',markersize=3,label = 'MESSENGER')
#plt.plot_date(ic_mo_start_time_num[iuly],ic.mo_sc_heliodistance[iuly],'ok',c='violet',markersize=3,label = 'Ulysses')

plt.ylabel('Heliocentric distance [AU]')
plt.xlabel('Year')
# ic_mo_start_time_num[iwin][100] en este indice comienza el 2018
plt.ylim([0,1.2])
#-plt.xlim([ic_mo_start_time_num[iwin][100],ic_mo_start_time_num[iwin][2]])
plt.ylim(0,1.6)
plt.legend(loc=3)




# ****************************************************************************
fig=plt.figure(4, figsize=(15,10), dpi=70)
ax = plt.subplot(111,projection='polar')

#plt.title('ICMECAT events [HEEQ longitude, AU]')
plt.title('ICME/shock events [[HEEQ] longitude ]')

#get indices for each target
#ivex=np.where(ic.sc_insitu=='VEX')[0]
#imav=np.where(ic.sc_insitu=='MAVEN')[0]
#bepii=np.where(ac.target_name=='BepiColombo')[0]


#markersize
ms=10
#alpha
al=0.7


ax.scatter(np.radians(icV['heliolongitude']),icV['distance'],s=ms,c='orange', alpha=al, label = 'Voyager 2')
#ax.scatter(np.radians(icP['heliolongitude']),icP['distance'],s=ms,c='purple', alpha=al, label = 'Pioneer')
ax.scatter(np.radians(icH['heliolongitude']),icH['distance'],s=ms,c='purple', alpha=al, label = 'Helios-1/2')


ax.scatter(np.radians(ic.mo_sc_long_heeq[imes]),ic.mo_sc_heliodistance[imes],s=ms,c='dimgrey', alpha=al, label = 'MESSENGER')
#-ax.scatter(np.radians(ic.mo_sc_long_heeq[ivex]),ic.mo_sc_heliodistance	[ivex],s=ms,c='orange', alpha=al)
ax.scatter(np.radians(ic.mo_sc_long_heeq[iwin]),ic.mo_sc_heliodistance[iwin],s=ms,c='mediumseagreen', alpha=al, label = 'Wind')
#-ax.scatter(np.radians(ic.mo_sc_long_heeq[imav]),ic.mo_sc_heliodistance	[imav],s=ms,c='orangered', alpha=al)

ax.scatter(np.radians(ic.mo_sc_long_heeq[ista]),ic.mo_sc_heliodistance[ista],s=ms,c='red', alpha=al, label = 'STA')
ax.scatter(np.radians(ic.mo_sc_long_heeq[istb]),ic.mo_sc_heliodistance[istb],s=ms,c='blue', alpha=al, label = 'STB')

#ax.scatter(np.radians(ic.mo_sc_long_heeq[ipsp]),ic.mo_sc_heliodistance[ipsp],s=ms,c='black', alpha=al, label = 'PSP')
#ax.scatter(np.radians(ic.mo_sc_long_heeq[isol]),ic.mo_sc_heliodistance[isol],s=ms,c='brown', alpha=al, label = 'Solar Orbiter')
#ax.scatter(np.radians(ac.target_heeq_lon[soloi]),ac.target_distance[soloi],s=ms,c='green', alpha=al)
#ax.scatter(np.radians(ac.target_heeq_lon[bepii]),ac.target_distance[bepii],s=ms,c='violet', alpha=al)
ax.scatter(np.radians(ic.mo_sc_long_heeq[iuly]),ic.mo_sc_heliodistance[iuly],s=ms,c='violet', alpha=al, label = 'Ulysses')

frame='HEEQ'
fsize=15
backcolor='black'

#plt.rgrids((0.1,0.2,0.3,0.4,0.6,0.8,1.0,1.2, 1.4,1.6,1.8,2.0),('','0.2','','0.4','0.6','0.8','1.0','1.2','1.4','','',''),angle=180, fontsize=fsize-4,alpha=0.8, ha='center',color=backcolor,zorder=5)
plt.thetagrids(range(0,360,45),(u'0\u00b0',u'45\u00b0',u'90\u00b0',u'135\u00b0',u'+/- 180\u00b0',u'- 135\u00b0',u'- 90\u00b0',u'- 45\u00b0'), fmt='%d',ha='center',fontsize=fsize,color=backcolor, zorder=5, alpha=1.0)




ax.text(0,0,'Sun', color='black', ha='center',fontsize=fsize-5,verticalalignment='top')
ax.text(0,1.1,'Earth', color='blue', ha='center',fontsize=fsize-5,verticalalignment='center')
ax.scatter(0,0,s=100,c='yellow',alpha=1, edgecolors='black', linewidth=0.3)


#plt.ylim([0,5.2])   #para Voyager
#plt.ylim([0,17.2]) #para pioneer 
plt.ylim([0,5.5])



plt.legend(loc=2)
plt.tight_layout()

plt.savefig('/Users/cperezal/Documents/Spacecraft_statistical/plotSH.eps',format='eps')




#http://www.fluxrope.info/




