from numpy import *
def lon180(lont,data):
## assume lon last
	lon=lont*1.
	lon[lon>180]=lon[lon>180]-360.
	ind=argsort(lon)
	data=data[...,ind]
	lon=lon[ind]
	return lon,data
