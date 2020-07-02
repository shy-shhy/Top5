def time_format(time):
    dic = time.split(':')
    hour = int(dic[0]) + 8
    if hour == 24:
        hour = 00
    min = dic[1]
    dic_time = str(hour)+ ":" +min
    return dic_time

