'''
Sia Ham, 1730812
Rhina Kim,1731848
R. Vincent, instructor
420-LCW-MS 
Programming Techniques and Applications
Final Project
'''


import datetime
import time


def get_2years():
    time_range = []
    day_sec = 60*60*24
    year_sec = day_sec*365

    now = datetime.datetime.now()
    unix_now = int(time.mktime(now.timetuple()))
    # print(unixtime_now) ... 1556403498 at the time 2019/04/27 18:18:00

    # we only need between now & (now - 2years ago)
    unix_start = unix_now - year_sec*2

    #calculate time range and make it into list
    for unix in range(unix_start, unix_now+day_sec, day_sec):
        Time = datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d')
        time_range.append(Time)
    #print(time_range)
    return time_range


#==============================================================================

### For example ###

#1970/01/01 00:00:00 => 0           ...0 sec since 1970/01/01 00:00:00
#=================================
#2012/01/01 00:00:00 => 1325376000  ...1325376000 sec since 1970/01/01 00:00:00
#2013/01/01 00:00:00 => 1356998400  ...1356998400 sec since 1970/01/01 00:00:00
#2014/01/01 00:00:00 => 1388534400  ...1388534400 sec since 1970/01/01 00:00:00
#2015/01/01 00:00:00 => 1420070400  ...1420070400 sec since 1970/01/01 00:00:00



### sample ###

if __name__ == "__main__":

    unix20120101 = 1325376000
    unix20130101 = 1356998400
    unix20140101 = 1388534400
    unix20150101 = 1420070400

    print("2013-2012: ", unix20130101 - unix20120101) # 31622400
    print("2014-2013: ", unix20140101 - unix20130101) # 31536000
    print("2015-2014: ", unix20150101 - unix20140101) # 31536000

    day_sec = 60*60*24
    year_sec = day_sec*365
    leap_year_sec = year_sec + day_sec

    print("day in second: ", day_sec)               # 86400
    print("year in second: ", year_sec)             # 31536000
    print("leap year in second: ", leap_year_sec)   # 31622400
