import pandas as pd

def gps_load(filename):
  colnames=['Date','finaltime','jday','x','xerr','y','yerr','z','zerr','corrcoeff','gipsy','stacov','file name','xy','xz','yz','preliminarysolution']
  data=pd.read_csv(filename,delim_whitespace=True,names=colnames)
  return data
