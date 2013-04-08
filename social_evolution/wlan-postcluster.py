#!/usr/bin/python

ap_clu_fid = open('wifi-ap-cluster.arff')
while True:
    file_line = ap_clu_fid.readline()
    if '@data' == file_line:
        break
ap_fid = open('wifi-ap-temp.csv')
ap_fid.readline()

ap_clu = {}

while True:
    ap_file_record_line = ap_fid.readline()
    ap_clu_record_line = ap_clu_fid.readline()
    if '' == ap_file_record_line:
        break
    ap_file_records = [record.strip() for record in ap_file_record_line.split(',')]
    ap_clu_records = [record.strip() for record in ap_clu_record_line.split(',')]
    ap_clu[ap_file_records[0]] = ap_clu_records[len(ap_clu_records) - 1]

ap_clu_fid.close()
ap_fid.close()
