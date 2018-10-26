#!/usr/bin/env python
#-*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join
import xlwt
import xlrd

# Input the txt file path
mypath = raw_input("Please input the txt file path:\n")
testfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath,f)) and f.endswith('.txt')]
print testfiles

for testfile in testfiles:
    f = open(testfile, 'r+')
    row_list = []

    for row in f:
        row_list.append(row.split())

    column_list = zip(*row_list)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('sheet1')

    i = 0
    for column in column_list:
        for item in range(len(column)):
            worksheet.write(item, i, column[item])
        i+=1

    workbook.save(testfile.replace('.txt','.xls'))
