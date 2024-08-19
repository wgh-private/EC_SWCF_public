def time2str(time):
    y = str(int(time[0]))
    m = str(int(time[1]))
    if time[1] < 10:
        m = '0'+m
    d = str(int(time[2]))
    if time[2] < 10:
        d = '0'+d
    ymd = y+m+d
    return ymd
