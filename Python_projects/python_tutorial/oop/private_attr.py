#!/usr/bin/python
# **** coding: utf-8 ****

class JustCounter:
    # Private var
    __secretCount = 0 
    # Public var
    publicCount = 0

    def count(self):
        self.__secretCount += 1
        self.publicCount += 1
        print self.__secretCount


counter = JustCounter()
counter.count()
counter.count()

print counter.publicCount
print counter.__secretCount
