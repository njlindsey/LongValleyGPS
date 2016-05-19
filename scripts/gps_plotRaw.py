import pandas as pd
from pandas import DataFrame, read_csv
import numpy as np
import matplotlib.pyplot as plt

# read the CSV-file into a DataFrame df
def gps_load(filename):
  colnames=['finaltime','jday','x','y','z','r','xerr','yerr','zerr','corrcoeff','gipsy','stacov','file name','xy','xz','yz','preliminarysolution']
  data=pd.read_csv(filename,delim_whitespace=True,names=colnames)
  return data

def gps_plotEastComponent(df,ax):
  ax.errorbar(df.jday, df.x, yerr=df.xerr, marker='o',linestyle='None',color='red',
    ecolor='grey', capthick=0, markersize=3,markeredgewidth=0.2)
  plt.ylabel('East (mm)')
  plt.grid(alpha=0.4)
  return ax

def gps_plotNorthComponent(df,ax):
  ax.errorbar(df.jday, df.y, yerr=df.yerr, marker='o',linestyle='None',color='blue',
      ecolor='grey', capthick=0, markersize=3,markeredgewidth=0.2)
  plt.ylabel('North (mm)')
  plt.grid(alpha=0.4)
  return ax

def gps_plotUpComponent(df,ax):
  ax.errorbar(df.jday, df.z, yerr=df.zerr, marker='o',linestyle='None',color='green',
      ecolor='grey', capthick=0, markersize=3,markeredgewidth=0.2)
  plt.ylabel('Up (mm)')
  plt.grid(alpha=0.4)
  return ax

def gps_plotRawTrendline(df):
  # plot raw
  ax1 = fig.add_subplot(311); ax1=gps_plotEastComponent(df,ax1)
  ax2 = fig.add_subplot(312); ax2=gps_plotNorthComponent(df,ax2)
  ax3 = fig.add_subplot(313); ax3=gps_plotUpComponent(df,ax3)
  # calc trendline
  xtrend=np.poly1d(np.polyfit(df.jday,df.x,1))
  ytrend=np.poly1d(np.polyfit(df.jday,df.y,1))
  ztrend=np.poly1d(np.polyfit(df.jday,df.z,1))
  # plot trendline
  nps = np.linspace(2004.75, 2017, 100)
  ax1.plot(nps,xtrend(nps),"k-"); ax2.plot(nps,ytrend(nps),"k-"); ax3.plot(nps,ztrend(nps),"k-")
  return ax1,ax2,ax3

##############################################################
df=gps_load("p589.rneu") #load

fig = plt.figure() #plot raw data with trendline
ax1,ax2,ax3=gps_plotRawTrendline(df)
plt.tight_layout()
plt.show()
