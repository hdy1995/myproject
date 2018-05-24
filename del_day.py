import datetime


def del_day(day1, day2):  # 根据xml文件内时间格式修改
    try:
        d1 = datetime.datetime.strptime(day1, '%a %b %d %H:%M:%S +0800 %Y')
        d2 = datetime.datetime.strptime(day2, '%a %b %d %H:%M:%S +0800 %Y')
        # d1 = datetime.datetime.strptime(day1, '%Y/%m/%d %H:%M:%S')
        # d2 = datetime.datetime.strptime(day2, '%Y/%m/%d %H:%M:%S')
        ans = d1 - d2
        return ans.days
    except TypeError:
        return 0
