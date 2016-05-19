import pandas as pd
from pandas import DataFrame, read_csv
import numpy as np
import matplotlib.pyplot as plt
import os
import math as m

#grab rneu filenames in cwd
def gps_getfilenames():
    files=[]
    for file in os.listdir('./'):
        if file.endswith('rneu'):
            files.append(file)
    return files

# read files into 1 dict of dataframes
def gps_loadAll(files):
    D={}
    for index,file in enumerate(files):
        colnames=['finaltime','jday','x','y','z','xerr','yerr','zerr']
        dic = pd.read_csv(file,names=colnames,delim_whitespace=True,header=None,usecols=[0,1,2,3,4,6,7,8])
        dic=dic.astype(np.float)
        D[index]=dic
    return D

# add vector as r and phi (polar coords) to each station's dataframe in the dict
def gps_calcVec(df):
    r=np.sqrt(df.x**2+df.y**2)
    phi=np.arctan(df.y/df.x)
    return r,phi
def gps_calcVecAll(df):
    for i in range(len(df)): #loop over stations
      r,phi=gps_calcVec(df[i]) #add vector columns to each dataframe
      df[i]['r']=r
      df[i]['phi']=phi
    return df

#plot vector in map and cross
def gps_findMatchTimes(df):
  jdayRounded=np.around(df.jday,decimals=2)
  for index,row in enumerate(jdayRounded):
    if row==round(t0,2):
      t0index=index
    if row==round(t1,2):
      t1index=index
  return t0index, t1index
def gps_plotVecMap(df,ax1,t0,t1):
    lat=[28.11393296,29.31393296,27.95]
    lon=[-96.33100599,-96.61100599,-97.69900]
    for i in range(len(df)): #loop over stations
      t0index,t1index=gps_findMatchTimes(df[i])
      ax1.quiver(lat[i],lon[i],df[i].r[t0index],df[i].phi[t0index],
        color='red')
      ax1.quiver(lat[i],lon[i],df[i].r[t1index],df[i].phi[t1index],
        color='red')
      ax1.quiver(lat[i],lon[i],df[i].r[t1index]-df[i].r[t0index],df[i].phi[t1index]-df[i].phi[t0index])
    return ax1
def gps_plotVecEarthing(df,ax2,t0,t1):
    return ax2
def gps_plotVecNorthing(df,ax3,t0,t1):
    return ax3
def gps_plotVecs(df,t0,t1):
    fig = plt.figure() #plot raw data with trendline
    ax1 = plt.subplot2grid((2,4),(0,0),colspan=2,rowspan=2);
    ax1=gps_plotVecMap(df,ax1,t0,t1)
    plt.show()
    ax2 = plt.subplot2grid((2,4),(0,2),colspan=2); ax2=gps_plotVecEasting(df,ax2,t0,t1)
    ax3 = plt.subplot2grid((2,4),(1,2),colspan=2); ax3=gps_plotVecNorthing(df,ax3,t0,t1)
    return fig,ax


##############################################################
files=gps_getfilenames() #get filenames
df=gps_loadAll(files)    #load dataframs from all files into 1 dict, to call: df[1].x
df=gps_calcVecAll(df)  #pass df dict to calc vector for each station at time of interest
t0=2011.4608; t1=2016.3377 #set times to difference
fig=gps_plotVecs(df,t0,t1)
plt.tight_layout()
fig.savefig("gps_Diff%s-%s.ps" % (time1,time0))
