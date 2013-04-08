#!/usr/bin/python

dyads = {}

fid = open('temp-relationship-09-05.csv')
fid.readline()
while True:
    string = fid.readline()
    if '' == string:
        break
    records = [word.strip() for word in string.split(',')]
    if 'SocializeTwicePerWeek' != records[2]:
        continue
    user1 = records[0]
    user2 = records[1]
    key1 = 'p' + user1 + ' - ' + 'p' + user2
    key2 = 'p' + user2 + ' - ' + 'p' + user1
    if key1 in dyads:
        dyads[key1] += 1
    else:
        dyads[key1] = 1
    if key2 in dyads:
        dyads[key2] += 1
    else:
        dyads[key2] = 1
fid.close()

scores_count = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
non_friend_count = 0
friend_count = 0
single_count = 0

fid1 = open('dyads-score.csv')
fid2 = open('matrix-after-process.csv')
fid2.readline()
while True:
    string1 = fid1.readline()
    string2 = fid2.readline()
    if '' == string2:
        break
    records1 = [word.strip() for word in string1.split(',')]
    records2 = [word.strip() for word in string2.split(',')]
    if records2[0] in dyads:
        if 2 == dyads[records2[0]]:
            column = 0
            friend_count += 1
        else:
            column = 2
            single_count += 1
    else:
        column = 1
        non_friend_count += 1
    score_this_loop = float(records1[2])
    if score_this_loop <= -1:
        row = 0
    elif score_this_loop <= 0.125:
        row = 1
    elif score_this_loop <= 1.25:
        row = 2
    elif score_this_loop <= 2.375:
        row = 3
    elif score_this_loop <= 3.5:
        row = 4
    elif score_this_loop <= 4.625:
        row = 5
    elif score_this_loop <= 5.75:
        row = 6
    elif score_this_loop <= 7:
        row = 7
    else:
        row = 8
    scores_count[row][column] += 1

wfid = open('bar-result.csv', 'w')
for count_row in scores_count:
    count_row[0] = 100 * float(count_row[0]) / friend_count
    count_row[1] = 100 * float(count_row[1]) / non_friend_count
    count_row[2] = 100 * float(count_row[2]) / single_count
    wfid.write(str(round(count_row[0], 2)) + ',' + str(round(count_row[1], 2)) + ',' + str(round(count_row[2], 2)) + '\n')
wfid.close()
