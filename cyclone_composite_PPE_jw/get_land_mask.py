from __future__ import absolute_import
from numpy import *
from scipy.interpolate import *

def get_land_mask(lat, lon):
    lon = lon*1.0
    lon[lon > 180] = lon[lon > 180]-360
    lon = sort(lon)
    import scipy.io
    topo = scipy.io.loadmat('/glade/u/home/dtmccoy/scripts/topofile.mat')
    lon_topo = array(topo['lon_topo'])
    lat_topo = array(topo['lat_topo'])
    topo = array(topo['topo'])
    [X, Y] = meshgrid(lat_topo, lon_topo)
    [Xq, Yq] = meshgrid(lat, lon)
    lsmaski = interp2d(lat_topo, lon_topo, topo)
    lsmask = lsmaski(lat, lon)
#	lsmask = griddata((X.flatten(),Y.flatten()),topo.flatten(),(Xq.flatten(),Yq.flatten()));
#	lsmask=reshape(lsmask,Xq.shape)
    lsmask[lsmask > 0] = NaN
    lsmask[lsmask <= 0] = 1
    lsmask = transpose(lsmask, [1, 0])
    return lsmask
