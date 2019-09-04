#!/usr/bin/python
# --- coding: utf-8 ----

fileName = "test.txt"
fileObj = open(fileName, 'w+')
# Write some info into the file
fileObj.write("guimin love xiaoqi\n guimin lovw God\n")
fileObj.close()
