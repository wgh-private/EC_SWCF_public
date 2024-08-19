# @Author: Geethma Werapitiya <wgeethma>
# @Date:   2023-08-02T17:16:05-06:00
# @Email:  wgeethma@uwyo.edu
# @Last modified by:   wgeethma
# @Last modified time: 2023-08-28T19:15:56-06:00

import time
from numpy import *
from time2str import *
#import iris
import datetime
import numpy as np
#from iris.time import PartialDateTime
#import glob
def get_slp(time1, member, varnm='PS'):
    wd = '/glade/campaign/uwyo/wyom0124/daily/PD/'+'PPE_rerun_ensemble_PD.'+member+'/atm/hist/'  #path of the directory where the PPD data is saved
    import netCDF4 as nc
    from datetime import datetime
    f = nc.MFDataset(wd+'*h1*nc', 'r')
    tvar = 'time'
    tt = f.variables[tvar]
    latvar = 'lat'
    lonvar = 'lon'
    lat = f.variables[latvar][:]
    lon = f.variables[lonvar][:]
    DATE=datetime(int(time1[0]), int(time1[1]), int(time1[2]),12)
    ind1 = nc.date2index(
        DATE, tt, select='nearest',calendar='gregorian')
    Z = f.variables[varnm][ind1]
    lon[lon > 180] = lon[lon > 180]-360
    ind = argsort(lon)
    lon = lon[ind]
    Z = 1.*Z[:,ind]
    ind2 = argsort(lat)
    Z = 1.*Z[ind2]
    lat = lat[ind2]
    return Z, lat, lon
