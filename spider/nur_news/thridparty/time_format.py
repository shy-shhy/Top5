def time_format(time):
    if time:
        dic = time.split(':')
        hour = int(dic[0]) + 8
        if hour >= 24:
            hour -= 24
        min = dic[1]
        dic_time = str(hour) + ":" + min
        return dic_time
    else:
        return ""

time_format('')

