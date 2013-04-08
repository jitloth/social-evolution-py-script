#!/usr/bin/python

import datetime

class matrix_record:
    def __init__(self):
        self.proximity_times_work = 0
        self.proximity_times_bed = 0
        self.proximity_times_worknight = 0
        self.proximity_times_weekendday = 0
        self.proximity_times_weekendnight = 0
        self.call_times = 0
        self.sms_times = 0

    def __str__(self):
        string_to_write = str(self.proximity_times_work) + ',' \
                        + str(self.proximity_times_bed) + ',' \
                        + str(self.proximity_times_worknight) + ',' \
                        + str(self.proximity_times_weekendday) + ',' \
                        + str(self.proximity_times_weekendnight) + ',' \
                        + str(self.call_times) + ',' \
                        + str(self.sms_times)
        return string_to_write

    def addOneProximity(self, datetime_str):
        temp_list = datetime_str.split(' ')
        ymd = temp_list[0].split('-')
        this_day = datetime.date(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        hms = temp_list[1].split(':')
        hour = int(hms[0])
        if (6 >= hour) or (23 <= hour):
            self.proximity_times_bed += 1
        elif (7 <= hour) and (17 >= hour):
            if 5 >= this_day.isoweekday():
                self.proximity_times_work += 1
            else:
                self.proximity_times_weekendday += 1
        else:
            if 5 >= this_day.isoweekday():
                self.proximity_times_worknight += 1
            else:
                self.proximity_times_weekendnight += 1

    def addOneCall(self, datetime_str):
        self.call_times += 1

    def addOneSMS(self, datetime_str):
        self.sms_times += 1

a2b_sms_dict = dict()

def process_file(file_name, column_property):
    fid = open(file_name)
    fid.readline()
    while True:
        record_string = fid.readline()
        if '' == record_string:
            break
        records = record_string.split(',')
        if records[0] == records[1]:
            continue
        if not records[0].startswith('sp') or not records[1].startswith('sp'):
            continue
        record_key1 = records[0] + ' : ' + records[1]
        record_key2 = records[1] + ' : ' + records[0]
        if record_key1 in a2b_sms_dict:
            obj = a2b_sms_dict[record_key1]
        elif record_key2 in a2b_sms_dict:
            obj = a2b_sms_dict[record_key2]
        else:
            obj = matrix_record()
            a2b_sms_dict[record_key1] = obj
        getattr(obj, 'addOne' + column_property)(records[2])
    fid.close()

# sms logs process
process_file('temp-sms.csv', 'SMS')

# call logs process
process_file('temp-call.csv', 'Call')

# proximity logs process
process_file('temp-proximity.csv', 'Proximity')

# write file to matrix
matrix_after_process = open('matrix-after-process.csv', 'w')
matrix_after_process.write('dyads,work,bed,worknight,weekendday,weekendnight,call,sms\n')
for dyads, matrix_row in a2b_sms_dict.items():
    matrix_after_process.write(dyads + ',' + str(matrix_row) + '\n')
matrix_after_process.close()
