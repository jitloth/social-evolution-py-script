#!/usr/bin/python

import datetime

def generate_timekey(datetime_str):
    temp = [part.strip() for part in datetime_str.split(' ')]
    ymd = temp[0].split('-')
    hms = temp[1].split(':')
    thisday = datetime.date(int(ymd[0]), int(ymd[1]), int(ymd[2]))
    return thisday.weekday() * 24 + int(hms[0])

timekey_max = 24 * 7

wifi_ap = {}

temp_cluster = []
unix_time_now = 0
user_now = 0
fid = open('WLAN2.csv')
fid.readline()
while True:
    record_line = fid.readline()
    if '' == record_line:
        break
    records = [word.strip() for word in record_line.split(',')]
    timekey = generate_timekey(records[1])
    ap = int(records[2])
    if ap not in wifi_ap:
        wifi_ap[ap] = [0 for x in range(timekey_max)]
    wifi_ap[ap][timekey] += 1
fid.close()

fid = open('wifi-ap-temp.csv', 'w')
title = '\"id\"'
for i in range(timekey_max):
    title = title + ',' + '\"' + str(i) + '\"'
title += '\n'
fid.write(title)
for ap_id, time_array in wifi_ap.items():
    sum_access = sum(time_array)
    if 5 > len([x for x in time_array if x > 0]):
        continue
    string_to_write = str(ap_id)
    for i in range(timekey_max):
        string_to_write = string_to_write + ',' + str(float(time_array[i]) / sum_access)
    string_to_write += '\n'
    fid.write(string_to_write)
fid.close()
