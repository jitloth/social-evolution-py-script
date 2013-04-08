#!/usr/bin/python

import datetime

timekey_max = 24 * 7

def generate_pairkey(user1, user2):
    bigger_number = max(int(user1), int(user2))
    smaller_number = min(int(user1), int(user2))
    return smaller_number * 100 + bigger_number

def generate_timekey(datetime_str):
    temp = [part.strip() for part in datetime_str.split(' ')]
    ymd = temp[0].split('-')
    hms = temp[1].split(':')
    thisday = datetime.date(int(ymd[0]), int(ymd[1]), int(ymd[2]))
    return thisday.weekday() * 24 + int(hms[0])

class dyad_record:
    def __init__(self):
        self.relation = 0
        self.time_prox = {}
        for i in range(timekey_max):
            self.time_prox[i] = 0

    def addRelationCount(self, records):
        if 'SocializeTwicePerWeek' == records[2]:
            self.relation += 1

    def getRelation(self):
        return self.relation

    def addProximityCount(self, records):
        self.time_prox[generate_timekey(records[2])] += 1

    def getProxDict(self):
        return self.time_prox

def process_file(file_type, dyads_matrix):
    fid = open(globals()[file_type + '_file_path'])
    fid.readline()
    while True:
        record_line = fid.readline()
        if '' == record_line:
            break
        records = [word.strip() for word in record_line.split(',')]
        user1 = records[globals()[file_type + '_user1_idx']]
        user2 = records[globals()[file_type + '_user2_idx']]
        if user1 == user2:
            continue
        key = generate_pairkey(user1, user2)
        if key in dyads_matrix:
            obj = dyads_matrix[key]
        else:
            obj = dyad_record()
            dyads_matrix[key] = obj
        getattr(obj, globals()[file_type + '_func'])(records)
    fid.close()

relation_file_path = 'temp-relationship-09-05.csv'
relation_user1_idx = 0
relation_user2_idx = 1
relation_func = 'addRelationCount'

prox_file_path = 'temp-proximity.csv'
prox_user1_idx = 0
prox_user2_idx = 1
prox_func = 'addProximityCount'

matrix = {}
process_file('relation', matrix)
process_file('prox', matrix)

prox = [[0 for x in range(timekey_max)] for y in range(3)]
relation_count = [0 for x in range(3)]

for dyad, record in matrix.items():
    for time_idx, prox_count in record.getProxDict().items():
        prox[record.getRelation()][time_idx] += prox_count
        relation_count[record.getRelation()] += 1

wfid = open('prox-time-analysi-2.csv', 'w')
for i in range(3):
    str_to_print = str(float(prox[i][0]) / relation_count[i])
    for j in range(1, timekey_max):
        str_to_print = str_to_print + ',' + str(float(prox[i][j]) / relation_count[i])
    str_to_print += '\n'
    wfid.write(str_to_print)
wfid.close()

wfid = open('prox-time-avg.csv', 'w')
for j in range(timekey_max):
    average = float(prox[0][j] + prox[1][j] + prox[2][j]) / (relation_count[0] + relation_count[1] + relation_count[2])
    wfid.write(str(average) + '\n')
wfid.close()
