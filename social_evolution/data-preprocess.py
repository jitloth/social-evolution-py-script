#!/usr/bin/python

import datetime

class dyads_record:
    def __init__(self):
        self.prox_workday = 0
        self.prox_worknight = 0
        self.prox_weekend = 0
        self.sms = 0
        self.call = 0
        self.activity = 0

    def __str__(self):
        string_to_return = str(self.prox_workday) + ',' \
                         + str(self.prox_worknight) + ',' \
                         + str(self.prox_weekend) + ',' \
                         + str(self.sms) + ',' \
                         + str(self.call) + ',' \
                         + str(self.activity)
        return string_to_return

    def addOneActivity(self, datetime_str):
        self.activity += 1

    def addOneSMS(self, records):
        self.sms += 1

    def addOneCall(self, records):
        self.call += 1

    def addOneProximity(self, records):
        temp_list = records[2].split(' ')
        ymd = temp_list[0].split('-')
        this_day = datetime.date(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        hms = temp_list[1].split(':')
        hour = int(hms[0])
        if 5 < this_day.isoweekday():
            self.prox_weekend += 1
        elif (8 <= hour) and (17 >= hour):
            self.prox_workday += 1
        else:
            self.prox_worknight += 1

    @staticmethod
    def get_header():
        string_to_return = 'workday,' \
                         + 'worknight,' \
                         + 'weekend,' \
                         + 'sms,' \
                         + 'call,' \
                         + 'activity'
        return string_to_return

dyads_matrix = {}

sms_file_path = 'temp-sms.csv'
sms_user1_idx = 0
sms_user2_idx = 3
sms_func = 'addOneSMS'

call_file_path = 'temp-calls.csv'
call_user1_idx = 0
call_user2_idx = 3
call_func = 'addOneCall'

prox_file_path = 'temp-proximity.csv'
prox_user1_idx = 0
prox_user2_idx = 1
prox_func = 'addOneProximity'

def generate_key(i, j):
    return 'p' + str(i) + ' - ' + 'p' + str(j)

def process_activity(activity_file_name):
    act_org_dict = {}

    afid = open(activity_file_name)
    afid.readline()
    while True:
        record_line = afid.readline()
        if '' == record_line:
            break
        records = [word.strip() for word in record_line.split(',')]
        key = records[1] + ' - ' + records[2]
        if not key in act_org_dict:
            act_org_dict[key] = []
        act_org_dict[key].append(int(records[0]))
    afid.close()

    for org_time, member_list in act_org_dict.items():
        for i in range(len(member_list)):
            for j in range(i + 1, len(member_list)):
                if member_list[i] == member_list[j]:
                    continue
                key1 = generate_key(member_list[i], member_list[j])
                key2 = generate_key(member_list[j], member_list[i])
                if key1 in dyads_matrix:
                    obj = dyads_matrix[key1]
                elif key2 in dyads_matrix:
                    obj = dyads_matrix[key2]
                else:
                    obj = dyads_record()
                    dyads_matrix[key1] = obj
                obj.addOneActivity(org_time.split('-')[1].strip())

def process_file(file_type):
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
        key1 = generate_key(user1, user2)
        key2 = generate_key(user2, user1)
        if key1 in dyads_matrix:
            obj = dyads_matrix[key1]
        elif key2 in dyads_matrix:
            obj = dyads_matrix[key2]
        else:
            obj = dyads_record()
            dyads_matrix[key1] = obj
        getattr(obj, globals()[file_type + '_func'])(records)
    fid.close()

# campus activity process
process_activity('temp-activity.csv')

# sms process
process_file('sms')

# call process
process_file('call')

# proximity process
process_file('prox')

# write matrix to file
rfid = open('matrix-after-process.csv', 'w')
rfid.write('dyads,' + dyads_record.get_header() + '\n')
for dyads, record in dyads_matrix.items():
    rfid.write(dyads + ',' + str(record) + '\n')
rfid.close()
