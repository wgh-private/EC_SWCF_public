# @Author: Geethma Werapitiya <wgeethma>
# @Date:   2023-08-08T15:59:12-06:00
# @Email:  wgeethma@uwyo.edu
# @Last modified by:   wgeethma
# @Last modified time: 2023-08-08T15:59:14-06:00

import time
import sys
from numpy.ma import *
import datetime
from numpy import *
from trax import *
from trax.trax import *
import get_slp_ppe_mfd
import warnings
from ymd2dayssince import dayssince2ymd
savedir='path of the directory to save composited cyclone data'
def composite_member(member,varrs=['TGCLDLWP','PRECC','PRECL','U10','TMQ','TGCLDIWP']):
    t1=time.perf_counter()
    N_LEN=1 #710  #number of days to get the composited for (use 710)
    DAYZERO=[2016,1,15]  #Starting date
    warnings.filterwarnings("ignore")
    compos=[NaN]*N_LEN
    member=int(member)
    memberstr=f"{member:03}"

    for i in range(N_LEN):
        ymd=dayssince2ymd(i,DAYZERO)
        print(ymd)
        compos[i]=composite_day(ymd,memberstr,varrs=varrs)
    dataout={}
    for i in range(len(varrs)):
        dataout[varrs[i]]=quick_process_composites(compos,varrs[i])
    dataout['OCEAN']=quick_process_composites(compos,'OCEAN')
    dataout['PS']=quick_process_composites(compos,'PS')

    # savez(savedir+'/ppe_compos_'+memberstr+'.npz',dataout=dataout)
    print('all saved')
    t2=time.perf_counter()
    print((t2-t1))
    return dataout

def quick_process_composites(compos,varnm):
    ## return composite, mean, count, time, N, lat,lon
    zz=compos[0][varnm]
    dict_compos={'comp':zz[0],'mean':zz[3][:,0],'lat':zz[4],'N':zz[1],'lon':zz[5],'time':zz[3][:,6:9]}
    for i in range(1,len(compos)):
        zz=compos[i][varnm]
        dict_compos['comp']=concatenate((dict_compos['comp'],zz[0]),axis=-1)
        dict_compos['N']=concatenate((dict_compos['N'],zz[1]),axis=-1)
        dict_compos['mean']=concatenate((dict_compos['mean'],zz[3][:,0]),axis=-1)
        dict_compos['lat']=concatenate((dict_compos['lat'],zz[4]),axis=-1)
        dict_compos['lon']=concatenate((dict_compos['lon'],zz[5]),axis=-1)
        dict_compos['time']=concatenate((dict_compos['time'],zz[3][:,6:9]),axis=0)
    dict_compos['coords']=zz[2]
    return dict_compos
#    statscyc = [np.mean(ZZ[ind]), NaN, NaN, NUM, latcent,
#                loncent, time[0], time[1], time[2]]
#    return statso[0], statsn[0], statscyc
def composite_day(time_in,member,varrs=['TGCLDLWP']):
    ## HACK for short time
    ##
    time_hack=[time_in[0],time_in[1],16]
    time_av=get_month_ymd(time_hack)
    SLP0=get_slp_ppe_mfd.get_slp(time_in,member)#[time_in.year,time_in.month,time_in.day])
    time_av=get_month_ymd(time_in)
    SLPM=zeros((len(time_av),SLP0[0].shape[0],SLP0[0].shape[1]))
    for  i in range(len(time_av)):
        SLPM[i]=get_slp_ppe_mfd.get_slp(time_av[i],member)[0]
    SLPP=SLP0[0]-nanmean(SLPM,axis=0)

    from get_land_mask import get_land_mask
    landmask=get_land_mask(SLP0[1],SLP0[2])

    DD2=GET_LAT_LON(SLPP,landmask*SLP0[0],SLP0[1],SLP0[2])

    # import matplotlib.pyplot as plt
    # plt.figure();
    # plt.pcolormesh(SLP0[2],SLP0[1],SLPP*landmask)
    # plt.colorbar()
    # plt.plot(DD2['lon'],DD2['lat'],'xr')

    composites={}
    for  i in range(len(varrs)):
        ZZ=get_slp_ppe_mfd.get_slp(time_in,member,varnm=varrs[i])
        COMPOS=do_composite(ZZ[0],ZZ[1],ZZ[2],time_in,DD2)
        composites[varrs[i]]=COMPOS
    composites['PS']=do_composite(SLP0[0],SLP0[1],SLP0[2],time_in,DD2)
    LAND=get_land_mask(SLP0[1],SLP0[2])
    composites['OCEAN']=do_composite(LAND,SLP0[1],SLP0[2],time_in,DD2)
    return composites
if __name__ == "__main__":
    composite_member(sys.argv[1])
