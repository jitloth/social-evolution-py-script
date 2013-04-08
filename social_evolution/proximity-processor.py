#!/usr/bin/python

import datetime

dyads_matrix = {}

def generate_key(i, j):
    return 'p' + str(i) + ' - ' + 'p' + str(j)

def generate_index(datetime_str):
    temp_list = datetime_str.split(' ')
    ymd = temp_list[0].split('-')
    this_day = datetime.date(int(ymd[0]), int(ymd[1]), int(ymd[2]))
    hms = temp_list[1].split(':')
    hour = int(hms[0])
    if 5 < this_day.isoweekday():
        i = 1
    else:
        i = 0
    return i * 24 + hour

fid = open('temp-proximity.csv')
fid.readline()
while True:
    record_line = fid.readline()
    if '' == record_line:
        break
    records = [word.strip() for word in record_line.split(',')]
    user1 = records[0]
    user2 = records[1]
    if user1 == user2:
        continue
    key1 = generate_key(user1, user2)
    key2 = generate_key(user2, user1)
    if key1 in dyads_matrix:
        array = dyads_matrix[key1]
    elif key2 in dyads_matrix:
        array = dyads_matrix[key2]
    else:
        array = [0 for x in range(48)]
        dyads_matrix[key1] = array
    array[generate_index(records[2])] += 1
fid.close()

dyads = {}
fid = open('temp-relationship-09-05.csv')
fid.readline()
while True:
    record_line = fid.readline()
    if '' == record_line:
        break
    records = [word.strip() for word in record_line.split(',')]
    if 'CloseFriend' != records[2]:
        continue
    user1 = records[0]
    user2 = records[1]
    if user1 == user2:
        continue
    key1 = generate_key(user1, user2)
    key2 = generate_key(user2, user1)
    if key1 in dyads:
        dyads[key1] = dyads[key2] = 2
    else:
        dyads[key1] = dyads[key2] = 1
fid.close()

fid = open('time-only.csv', 'w')
for pair, array in dyads_matrix.items():
    if (not pair in dyads) or (2 != dyads[pair]):
        continue
    string = pair
    for entry in array:
        string = string + ',' + str(entry)
    string += '\n'
    fid.write(string)
for pair, array in dyads_matrix.items():
    if pair in dyads:
        continue
    string = pair
    for entry in array:
        string = string + ',' + str(entry)
    string += '\n'
    fid.write(string)
fid.close()
