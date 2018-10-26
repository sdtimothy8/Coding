#!/usr/bin/env python
#codding: utf-8

import os
import xlwt
import xlrd

a = [1, 2, 3]
b = [4, 5, 6]
c = [7, 8, 9]

row_list = []
row_list.append(a)
row_list.append(b)
row_list.append(c)

print row_list

column_list = zip(*row_list)

print column_list

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('sheet1')

i = 0
for column in column_list:
    for item in range(len(column)):
        worksheet.write(item, i, column[item])
    i = i + 1

workbook.save('zip.xls')
