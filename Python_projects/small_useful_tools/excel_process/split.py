#!/usr/bin/env python
#coding: utf-8

import os

testfile = 'test.txt'
f = open(testfile, 'r+')
row_list = []
for row in f:
    row_list.append(row.split())

print row_list

a = "love"
b = "jiale"

print join(a,b)
