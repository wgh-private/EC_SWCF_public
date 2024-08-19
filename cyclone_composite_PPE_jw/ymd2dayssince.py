from __future__ import absolute_import
from six.moves import range
from numpy import *
def time2fracy(timevec, **kwargs):
    import datetime
    dt = zeros(timevec.shape[0])*NaN
    for i in range(len(dt)):
        basedate = datetime.datetime(int(timevec[i, 0]), 1, 1)
        timed = datetime.datetime(int(timevec[i, 0]), int(
            timevec[i, 1]), int(timevec[i, 2]))
        dttemp = timed-basedate
        if kwargs.get('doy', False) == False:
            dt[i] = timevec[i, 0]+(dttemp.days)/365.
        else:
            dt[i] = dttemp.days
    return dt


def doy2dt(y, doy):
    import datetime
    basedate = datetime.datetime(y, 1, 1)
    nt = basedate+datetime.timedelta(days=doy-1)
    timevec = [nt.year, nt.month, nt.day]
    return nt


def doy2ymd(y, doy):
    import datetime
    basedate = datetime.datetime(y, 1, 1)
    nt = basedate+datetime.timedelta(days=doy-1)
    timevec = [nt.year, nt.month, nt.day]
    return timevec


def ymd2doy(time):
    import datetime
    basedate = datetime.datetime(time[0], 1, 1)
    tn = datetime.datetime(time[0], time[1], time[2])
    dt = tn-basedate
    doy = dt.days+1
    return doy


def ymd2dayssince(timevec):
    import datetime
    basedate = datetime.datetime(1970, 1, 1)
    dt = zeros(timevec.shape[0])*NaN
    for i in range(len(dt)):
        timed = datetime.datetime(int(timevec[i, 0]), int(
            timevec[i, 1]), int(timevec[i, 2]))
        dttemp = timed-basedate
        dt[i] = dttemp.days
    return dt


def dayssince2ymd(time, basedate):
    import datetime
    basedate = datetime.datetime(basedate[0], basedate[1], basedate[2])
    dt = datetime.timedelta(days=time)+basedate
    return [dt.year, dt.month, dt.day]


#def dayssince2ymd_nctime(time_in_dt, basedate):
#    import netcdftime as nctime
#    basedate = nctime.datetime(basedate[0], basedate[1], basedate[2])
#    basedatejd = nctime.JulianDayFromDate(basedate)
#    ymd = nctime.DateFromJulianDay(basedatejd+time_in_dt)
#    return ymd
