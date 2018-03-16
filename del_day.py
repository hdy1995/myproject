import datetime


def del_day(day1, day2):
    d1 = datetime.datetime.strptime(day1, '%Y/%m/%d %H:%M:%S')
    d2 = datetime.datetime.strptime(day2, '%Y/%m/%d %H:%M:%S')
    ans = d1 - d2
    return ans.days

