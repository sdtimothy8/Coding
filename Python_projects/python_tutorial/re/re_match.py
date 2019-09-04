#!/usr/bin/python
# **** coding: utf-8 ****

import re

line = "Cats are smarter than dogs"

matchObj = re.match( r'(.*) are (.*?) .*', line, re.I|re.M )

if matchObj:
    print "matchObj.group() : ", matchObj.group()
else:
    print "No match!"



str1 = "abrt.service"
str2 = "atd"
str3 = "atd.service ls"
str4 = " atd"

#matched = re.match( r'[^ \t]{1,128}(\.service)?', str3, re.I |re.M )
matched = re.match( r'[\s]*[\S]{,128}$', str4, re.I |re.M )
if matched:
    print "mathched.group(): ", matched.group() 
else:
    print "NOT matched!"

