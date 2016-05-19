import pandas as pd
from pandas import DataFrame, read_csv
import numpy as np
import matplotlib.pyplot as plt
import os

# read the CSV-file into a DataFrame df
def gps_load(filename):
  colnames=['finaltime','jday','x','y','z','r','xerr','yerr','zerr','corrcoeff','gipsy','stacov','file name','xy','xz','yz','preliminarysolution']
  data=pd.read_csv(filename,delim_whitespace=True,names=colnames)
  return data

def gps_plotEastComponent(df,ax):
  ax.errorbar(df.jday, df.x, yerr=df.xerr, marker='o',linestyle='None',color='red',
    ecolor='grey', capthick=0, markersize=4,markeredgewidth=0)
  plt.ylabel('East (mm)')
  plt.grid(alpha=0.4)
  return ax

def gps_plotNorthComponent(df,ax):
  ax.errorbar(df.jday, df.y, yerr=df.yerr, marker='o',linestyle='None',color='lightblue',
      ecolor='grey', capthick=0, markersize=4,markeredgewidth=0)
  plt.ylabel('North (mm)')
  plt.grid(alpha=0.4)
  return ax

def gps_plotUpComponent(df,ax):
  ax.errorbar(df.jday, df.z, yerr=df.zerr, marker='o',linestyle='None',color='lightgreen',
      ecolor='grey', capthick=0, markersize=4,markeredgewidth=0)
  plt.ylabel('Up (mm)')
  plt.grid(alpha=0.4)
  return ax

def gps_plotRawTrendline(df,fig):
  # plot raw
  ax1 = fig.add_subplot(311); ax1=gps_plotEastComponent(df,ax1)
  ax2 = fig.add_subplot(312); ax2=gps_plotNorthComponent(df,ax2)
  ax3 = fig.add_subplot(313); ax3=gps_plotUpComponent(df,ax3)
  # calc trendline
  xtrend=np.poly1d(np.polyfit(df.jday,df.x,1))
  ytrend=np.poly1d(np.polyfit(df.jday,df.y,1))
  ztrend=np.poly1d(np.polyfit(df.jday,df.z,1))
  # plot trendline
  nps = np.linspace(df.jday[1], df.jday[1], 100)
  ax1.plot(nps,xtrend(nps),"k-"); ax2.plot(nps,ytrend(nps),"k-"); ax3.plot(nps,ztrend(nps),"k-")
  return ax1,ax2,ax3

##############################################################
files=[]
for file in os.listdir('./'):
    if file.endswith('rneu'):
        files.append(file)
for file in files:
    df=gps_load(file)
    fig = plt.figure() #plot raw data with trendline
    ax1,ax2,ax3=gps_plotRawTrendline(df,fig)
    plt.tight_layout()
    fig.savefig("%s.ps" % file)
